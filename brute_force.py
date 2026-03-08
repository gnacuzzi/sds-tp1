from particle import Particle
from geometry import are_neighbors, are_neighbors_periodic


def brute_force_neighbors(particles: list[Particle], rc: float) -> dict[int, list[int]]:
    neighbors = {p.id: [] for p in particles}

    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            p1 = particles[i]
            p2 = particles[j]

            if are_neighbors(p1, p2, rc):
                neighbors[p1.id].append(p2.id)
                neighbors[p2.id].append(p1.id)

    return neighbors


def brute_force_neighbors_periodic(
    particles: list[Particle], rc: float, L: float
) -> dict[int, list[int]]:
    neighbors = {p.id: [] for p in particles}

    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            p1 = particles[i]
            p2 = particles[j]

            if are_neighbors_periodic(p1, p2, rc, L):
                neighbors[p1.id].append(p2.id)
                neighbors[p2.id].append(p1.id)

    return neighbors