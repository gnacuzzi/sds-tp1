#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

#include "generator.h"

static double random_uniform(double min, double max) {
    return min + (max - min) * ((double) rand() / RAND_MAX);
}

static int overlaps(Particle *particles, int count, double x, double y, double radius) {
    for (int i = 0; i < count; i++) {
        double dx = particles[i].x - x;
        double dy = particles[i].y - y;

        double dist = sqrt(dx * dx + dy * dy);

        if (dist < (particles[i].radius + radius)) {
            return 1;
        }
    }
    return 0;
}

Particle *generate_particles(int n, double L, double r_min, double r_max) {

    Particle *particles = malloc(n * sizeof(Particle));
    if (particles == NULL) {
        fprintf(stderr, "Error allocating particles\n");
        return NULL;
    }

    for (int i = 0; i < n; i++) {

        double x, y, radius;

        int valid_position = 0;

        while (!valid_position) {

            radius = random_uniform(r_min, r_max);

            x = random_uniform(radius, L - radius);
            y = random_uniform(radius, L - radius);

            if (!overlaps(particles, i, x, y, radius)) {
                valid_position = 1;
            }
        }

        particles[i].id = i;
        particles[i].x = x;
        particles[i].y = y;
        particles[i].radius = radius;
        particles[i].property = 0.0;
        particles[i].vx = 0.0;
        particles[i].vy = 0.0;
    }

    return particles;
}