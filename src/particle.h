#ifndef PARTICLE_H
#define PARTICLE_H

typedef struct {
    int id;
    double x;
    double y;
    double radius;
    double property;
    double vx;
    double vy;
} Particle;

#endif