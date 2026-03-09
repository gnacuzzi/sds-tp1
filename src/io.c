#include <stdio.h>
#include <stdlib.h>

#include "io.h"

void write_static_file(const char *filename, Particle *particles, int n, double L) {

    FILE *file = fopen(filename, "w");

    if (file == NULL) {
        fprintf(stderr, "Error opening static file %s\n", filename);
        return;
    }

    fprintf(file, "%d\n", n);
    fprintf(file, "%f\n", L);

    for (int i = 0; i < n; i++) {
        fprintf(file, "%f %f\n",
                particles[i].radius,
                particles[i].property);
    }

    fclose(file);
}

void write_dynamic_file(const char *filename, Particle *particles, int n, double t) {

    FILE *file = fopen(filename, "w");

    if (file == NULL) {
        fprintf(stderr, "Error opening dynamic file %s\n", filename);
        return;
    }

    fprintf(file, "%f\n", t);

    for (int i = 0; i < n; i++) {
        fprintf(file, "%f %f %f %f\n",
                particles[i].x,
                particles[i].y,
                particles[i].vx,
                particles[i].vy);
    }

    fclose(file);
}

void write_neighbors_file(const char *filename, int **neighbors, int *neighbor_count, int n) {

    FILE *file = fopen(filename, "w");

    if (file == NULL) {
        fprintf(stderr, "Error opening neighbors file %s\n", filename);
        return;
    }

    for (int i = 0; i < n; i++) {

        fprintf(file, "[%d", i);

        for (int j = 0; j < neighbor_count[i]; j++) {
            fprintf(file, " %d", neighbors[i][j]);
        }

        fprintf(file, "]\n");
    }

    fclose(file);
}