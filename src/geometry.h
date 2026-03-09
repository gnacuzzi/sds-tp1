#ifndef GEOMETRY_H
#define GEOMETRY_H

#include "particle.h"

double center_distance(Particle p1, Particle p2);

double border_distance(Particle p1, Particle p2);

int are_neighbors(Particle p1, Particle p2, double rc);

double center_distance_periodic(Particle p1, Particle p2, double L);

double border_distance_periodic(Particle p1, Particle p2, double L);

int are_neighbors_periodic(Particle p1, Particle p2, double rc, double L);

#endif