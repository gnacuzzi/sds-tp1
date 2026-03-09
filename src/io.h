#ifndef IO_H
#define IO_H

#include "particle.h"

void write_static_file(const char *filename, Particle *particles, int n, double L);
void write_dynamic_file(const char *filename, Particle *particles, int n, double t);
void write_neighbors_file(const char *filename, int **neighbors, int *neighbor_count, int n);

#endif