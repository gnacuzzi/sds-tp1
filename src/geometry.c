#include <math.h>

#include "geometry.h"

double center_distance(Particle p1, Particle p2) {
    double dx = p1.x - p2.x;
    double dy = p1.y - p2.y;

    return sqrt(dx * dx + dy * dy);
}

double border_distance(Particle p1, Particle p2) {
    return center_distance(p1, p2) - p1.radius - p2.radius;
}

int are_neighbors(Particle p1, Particle p2, double rc) {
    return border_distance(p1, p2) < rc;
}

double center_distance_periodic(Particle p1, Particle p2, double L) {
    double dx = p1.x - p2.x;
    double dy = p1.y - p2.y;

    dx = dx - L * round(dx / L);
    dy = dy - L * round(dy / L);

    return sqrt(dx * dx + dy * dy);
}

double border_distance_periodic(Particle p1, Particle p2, double L) {
    return center_distance_periodic(p1, p2, L) - p1.radius - p2.radius;
}

int are_neighbors_periodic(Particle p1, Particle p2, double rc, double L) {
    return border_distance_periodic(p1, p2, L) < rc;
}