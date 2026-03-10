#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#include "particle.h"
#include "generator.h"
#include "io.h"
#include "brute_force.h"
#include "cim.h"
#include "experiment.h"

#define STATIC_FILE "data/static.txt"
#define DYNAMIC_FILE "data/dynamic.txt"
#define BF_FILE "data/neighbors_bruteforce.txt"
#define CIM_FILE "data/neighbors_cim.txt"

static int **allocate_int_matrix(int rows, int cols) {
    int **matrix = malloc(rows * sizeof(int *));
    if (matrix == NULL) {
        return NULL;
    }

    for (int i = 0; i < rows; i++) {
        matrix[i] = malloc(cols * sizeof(int));
        if (matrix[i] == NULL) {
            for (int j = 0; j < i; j++) {
                free(matrix[j]);
            }
            free(matrix);
            return NULL;
        }
    }

    return matrix;
}

static void free_int_matrix(int **matrix, int rows) {
    if (matrix == NULL) {
        return;
    }

    for (int i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
}

static int compare_ints(const void *a, const void *b) {
    int int_a = *(const int *)a;
    int int_b = *(const int *)b;

    return int_a - int_b;
}

static void sort_neighbor_lists(int **neighbors, int *neighbor_count, int n) {
    for (int i = 0; i < n; i++) {
        qsort(neighbors[i], neighbor_count[i], sizeof(int), compare_ints);
    }
}

static int compare_neighbor_lists(
    int **neighbors_a,
    int *counts_a,
    int **neighbors_b,
    int *counts_b,
    int n
) {
    for (int i = 0; i < n; i++) {
        if (counts_a[i] != counts_b[i]) {
            return 0;
        }

        for (int j = 0; j < counts_a[i]; j++) {
            if (neighbors_a[i][j] != neighbors_b[i][j]) {
                return 0;
            }
        }
    }

    return 1;
}

static void print_usage(const char *program_name) {
    printf("Usage: %s [N] [M] [periodic]\n", program_name);
    printf("  N         Number of particles (default: 100)\n");
    printf("  M         Number of cells per dimension (default: 10)\n");
    printf("  periodic  0 = walls, 1 = periodic boundaries (default: 0)\n");
    printf("  L         Change L value\n");
    printf("  rc        Change rc value\n" );
}

int main(int argc, char *argv[]) {
    printf("Arguments %d\n", argc);

    if (argc > 1 && strcmp(argv[1], "experiment") == 0) {
        run_experiment();
        return 0;
    }

    int N = 100;
    int M = 10;
    int periodic = 0;

    double L = 20.0;
    double rc = 1.0;
    double r_min = 0.23;
    double r_max = 0.26;

    if (argc > 1) {
        N = atoi(argv[1]);
    }
    if (argc > 2) {
        M = atoi(argv[2]);
    }
    if (argc > 3) {
        periodic = atoi(argv[3]);
    }
    if (argc > 4) {
        L = (double)atoi(argv[4]);
        return 1;
    }
    if (argc > 5){
        rc = (double)atoi(argv[5]);
    }

    if (argc > 6){
        print_usage(argv[0]);
        return 1;
    } 

    if (N <= 0 || M <= 0 || (periodic != 0 && periodic != 1)) {
        print_usage(argv[0]);
        return 1;
    }

    /*
     * Safe CIM criterion for non-point particles:
     * L / M > rc + 2 * r_max
     */
    double cell_size = L / (double) M;
    double min_required_cell_size = rc + 2.0 * r_max;

    if (cell_size <= min_required_cell_size) {
        fprintf(stderr,
                "Error: invalid M for CIM.\n"
                "Current cell size L/M = %.6f, but it must be > %.6f\n"
                "(using rc + 2*r_max).\n",
                cell_size, min_required_cell_size);
        return 1;
    }

    srand((unsigned int) time(NULL));

    Particle *particles = generate_particles(N, L, r_min, r_max);
    if (particles == NULL) {
        fprintf(stderr, "Error generating particles\n");
        return 1;
    }

    write_static_file(STATIC_FILE, particles, N, L);
    write_dynamic_file(DYNAMIC_FILE, particles, N, 0.0);

    int **neighbors_bf = allocate_int_matrix(N, N);
    int **neighbors_cim = allocate_int_matrix(N, N);

    int *neighbor_count_bf = malloc(N * sizeof(int));
    int *neighbor_count_cim = malloc(N * sizeof(int));

    if (neighbors_bf == NULL || neighbors_cim == NULL ||
        neighbor_count_bf == NULL || neighbor_count_cim == NULL) {
        fprintf(stderr, "Error allocating neighbor structures\n");
        free(particles);
        free_int_matrix(neighbors_bf, N);
        free_int_matrix(neighbors_cim, N);
        free(neighbor_count_bf);
        free(neighbor_count_cim);
        return 1;
    }

    clock_t start_bf = clock();

    if (periodic) {
        brute_force_neighbors_periodic(
            particles, N, rc, L, neighbors_bf, neighbor_count_bf
        );
    } else {
        brute_force_neighbors(
            particles, N, rc, neighbors_bf, neighbor_count_bf
        );
    }

    clock_t end_bf = clock();

    clock_t start_cim = clock();

    if (periodic) {
        cim_neighbors_periodic(
            particles, N, L, M, rc, neighbors_cim, neighbor_count_cim
        );
    } else {
        cim_neighbors(
            particles, N, L, M, rc, neighbors_cim, neighbor_count_cim
        );
    }

    clock_t end_cim = clock();

    double brute_force_time = (double)(end_bf - start_bf) / CLOCKS_PER_SEC;
    double cim_time = (double)(end_cim - start_cim) / CLOCKS_PER_SEC;

    sort_neighbor_lists(neighbors_bf, neighbor_count_bf, N);
    sort_neighbor_lists(neighbors_cim, neighbor_count_cim, N);

    write_neighbors_file(BF_FILE, neighbors_bf, neighbor_count_bf, N);
    write_neighbors_file(CIM_FILE, neighbors_cim, neighbor_count_cim, N);

    int match = compare_neighbor_lists(
        neighbors_bf,
        neighbor_count_bf,
        neighbors_cim,
        neighbor_count_cim,
        N
    );

    printf("N = %d\n", N);
    printf("M = %d\n", M);
    printf("L = %.2f\n", L);
    printf("rc = %.2f\n", rc);
    printf("Periodic boundaries = %s\n", periodic ? "yes" : "no");
    printf("Cell size L/M = %.6f\n", cell_size);
    printf("Brute Force time: %.6f s\n", brute_force_time);
    printf("CIM time:         %.6f s\n", cim_time);
    printf("\n");

    if (match) {
        printf("Neighbor lists match between Brute Force and CIM.\n");
    } else {
        printf("Neighbor lists DO NOT match between Brute Force and CIM.\n");
    }

    printf("\n");
    printf("Files written:\n");
    printf(" - %s\n", STATIC_FILE);
    printf(" - %s\n", DYNAMIC_FILE);
    printf(" - %s\n", BF_FILE);
    printf(" - %s\n", CIM_FILE);

    free(particles);
    free_int_matrix(neighbors_bf, N);
    free_int_matrix(neighbors_cim, N);
    free(neighbor_count_bf);
    free(neighbor_count_cim);

    return 0;
}