#ifndef CIM_H
#define CIM_H

#include "particle.h"

void cim_neighbors(
    Particle *particles,
    int n,
    double L,
    int M,
    double rc,
    int **neighbors,
    int *neighbor_count
);

void cim_neighbors_periodic(
    Particle *particles,
    int n,
    double L,
    int M,
    double rc,
    int **neighbors,
    int *neighbor_count
);

#endif