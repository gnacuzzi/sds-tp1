#include "brute_force.h"
#include "geometry.h"

static void initialize_neighbor_counts(int *neighbor_count, int n) {
    for (int i = 0; i < n; i++) {
        neighbor_count[i] = 0;
    }
}

void brute_force_neighbors(
    Particle *particles,
    int n,
    double rc,
    int **neighbors,
    int *neighbor_count
) {
    initialize_neighbor_counts(neighbor_count, n);

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (are_neighbors(particles[i], particles[j], rc)) {
                neighbors[i][neighbor_count[i]] = j;
                neighbor_count[i]++;

                neighbors[j][neighbor_count[j]] = i;
                neighbor_count[j]++;
            }
        }
    }
}

void brute_force_neighbors_periodic(
    Particle *particles,
    int n,
    double rc,
    double L,
    int **neighbors,
    int *neighbor_count
) {
    initialize_neighbor_counts(neighbor_count, n);

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (are_neighbors_periodic(particles[i], particles[j], rc, L)) {
                neighbors[i][neighbor_count[i]] = j;
                neighbor_count[i]++;

                neighbors[j][neighbor_count[j]] = i;
                neighbor_count[j]++;
            }
        }
    }
}