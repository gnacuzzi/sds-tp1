#ifndef BRUTE_FORCE_H
#define BRUTE_FORCE_H

#include "particle.h"

void brute_force_neighbors(
    Particle *particles,
    int n,
    double rc,
    int **neighbors,
    int *neighbor_count
);

void brute_force_neighbors_periodic(
    Particle *particles,
    int n,
    double rc,
    double L,
    int **neighbors,
    int *neighbor_count
);

#endif