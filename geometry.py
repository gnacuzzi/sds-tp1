import math
from particle import Particle


def center_distance(p1: Particle, p2: Particle) -> float:
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return math.sqrt(dx * dx + dy * dy)


def border_distance(p1: Particle, p2: Particle) -> float:
    return center_distance(p1, p2) - p1.radius - p2.radius


def are_neighbors(p1: Particle, p2: Particle, rc: float) -> bool:
    return border_distance(p1, p2) < rc


def overlaps(p1: Particle, p2: Particle) -> bool:
    return center_distance(p1, p2) < (p1.radius + p2.radius)


def center_distance_periodic(p1: Particle, p2: Particle, L: float) -> float:
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dx = dx - L * round(dx / L)
    dy = dy - L * round(dy / L)

    return math.sqrt(dx * dx + dy * dy)


def border_distance_periodic(p1: Particle, p2: Particle, L: float) -> float:
    return center_distance_periodic(p1, p2, L) - p1.radius - p2.radius


def are_neighbors_periodic(p1: Particle, p2: Particle, rc: float, L: float) -> bool:
    return border_distance_periodic(p1, p2, L) < rc