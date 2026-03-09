#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "experiment.h"
#include "particle.h"
#include "generator.h"
#include "brute_force.h"
#include "cim.h"

#define RUNS 20

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

void run_experiment(void) {
    double L = 20.0;
    double rc = 1.0;
    double r_min = 0.23;
    double r_max = 0.26;
    int periodic = 0;

    /*
     * Study 1: vary N, keep M fixed
     */
    int N_values[] = {100, 200, 400, 600, 800};
    int num_N_values = sizeof(N_values) / sizeof(N_values[0]);
    int M_fixed = 10;

    /*
     * Study 2: vary M, keep N fixed
     * Keep M <= 13 because of the safe condition:
     * L / M > rc + 2*r_max
     */
    int M_values[] = {2, 4, 6, 8, 10, 12};
    int num_M_values = sizeof(M_values) / sizeof(M_values[0]);
    int N_fixed = 800;

    FILE *file = fopen("data/performance.csv", "w");
    if (file == NULL) {
        fprintf(stderr, "Error opening data/performance.csv\n");
        return;
    }

    fprintf(file, "study,N,M,method,run,time_seconds\n");

    /*
     * --------------------------------------------------
     * Study 1: vary N
     * --------------------------------------------------
     */
    for (int ni = 0; ni < num_N_values; ni++) {
        int N = N_values[ni];

        printf("Running vary_N experiment for N = %d, M = %d\n", N, M_fixed);

        for (int run = 0; run < RUNS; run++) {
            Particle *particles = generate_particles(N, L, r_min, r_max);
            if (particles == NULL) {
                fprintf(stderr, "Error generating particles\n");
                fclose(file);
                return;
            }

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
                fclose(file);
                return;
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
                    particles, N, L, M_fixed, rc, neighbors_cim, neighbor_count_cim
                );
            } else {
                cim_neighbors(
                    particles, N, L, M_fixed, rc, neighbors_cim, neighbor_count_cim
                );
            }
            clock_t end_cim = clock();

            double brute_force_time = (double)(end_bf - start_bf) / CLOCKS_PER_SEC;
            double cim_time = (double)(end_cim - start_cim) / CLOCKS_PER_SEC;

            fprintf(file, "vary_N,%d,%d,brute_force,%d,%.10f\n",
                    N, M_fixed, run + 1, brute_force_time);
            fprintf(file, "vary_N,%d,%d,cim,%d,%.10f\n",
                    N, M_fixed, run + 1, cim_time);

            free(particles);
            free_int_matrix(neighbors_bf, N);
            free_int_matrix(neighbors_cim, N);
            free(neighbor_count_bf);
            free(neighbor_count_cim);
        }
    }

    /*
     * --------------------------------------------------
     * Study 2: vary M
     * --------------------------------------------------
     */
    for (int mi = 0; mi < num_M_values; mi++) {
        int M = M_values[mi];

        printf("Running vary_M experiment for N = %d, M = %d\n", N_fixed, M);

        for (int run = 0; run < RUNS; run++) {
            Particle *particles = generate_particles(N_fixed, L, r_min, r_max);
            if (particles == NULL) {
                fprintf(stderr, "Error generating particles\n");
                fclose(file);
                return;
            }

            int **neighbors_bf = allocate_int_matrix(N_fixed, N_fixed);
            int **neighbors_cim = allocate_int_matrix(N_fixed, N_fixed);
            int *neighbor_count_bf = malloc(N_fixed * sizeof(int));
            int *neighbor_count_cim = malloc(N_fixed * sizeof(int));

            if (neighbors_bf == NULL || neighbors_cim == NULL ||
                neighbor_count_bf == NULL || neighbor_count_cim == NULL) {
                fprintf(stderr, "Error allocating neighbor structures\n");
                free(particles);
                free_int_matrix(neighbors_bf, N_fixed);
                free_int_matrix(neighbors_cim, N_fixed);
                free(neighbor_count_bf);
                free(neighbor_count_cim);
                fclose(file);
                return;
            }

            clock_t start_bf = clock();
            if (periodic) {
                brute_force_neighbors_periodic(
                    particles, N_fixed, rc, L, neighbors_bf, neighbor_count_bf
                );
            } else {
                brute_force_neighbors(
                    particles, N_fixed, rc, neighbors_bf, neighbor_count_bf
                );
            }
            clock_t end_bf = clock();

            clock_t start_cim = clock();
            if (periodic) {
                cim_neighbors_periodic(
                    particles, N_fixed, L, M, rc, neighbors_cim, neighbor_count_cim
                );
            } else {
                cim_neighbors(
                    particles, N_fixed, L, M, rc, neighbors_cim, neighbor_count_cim
                );
            }
            clock_t end_cim = clock();

            double brute_force_time = (double)(end_bf - start_bf) / CLOCKS_PER_SEC;
            double cim_time = (double)(end_cim - start_cim) / CLOCKS_PER_SEC;

            fprintf(file, "vary_M,%d,%d,brute_force,%d,%.10f\n",
                    N_fixed, M, run + 1, brute_force_time);
            fprintf(file, "vary_M,%d,%d,cim,%d,%.10f\n",
                    N_fixed, M, run + 1, cim_time);

            free(particles);
            free_int_matrix(neighbors_bf, N_fixed);
            free_int_matrix(neighbors_cim, N_fixed);
            free(neighbor_count_bf);
            free(neighbor_count_cim);
        }
    }

    fclose(file);

    printf("Experiment finished.\n");
    printf("Results written to data/performance.csv\n");
}