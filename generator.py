import random
from particle import Particle
from geometry import overlaps


def generate_particles(n: int, L: float, r_min: float, r_max: float) -> list[Particle]:
    particles = []

    while len(particles) < n:
        radius = random.uniform(r_min, r_max)

        x = random.uniform(radius, L - radius)
        y = random.uniform(radius, L - radius)

        candidate = Particle(
            id=len(particles),
            x=x,
            y=y,
            radius=radius,
            property=0.0,
            vx=0.0,
            vy=0.0
        )

        collision = False

        for p in particles:
            if overlaps(candidate, p):
                collision = True
                break

        if not collision:
            particles.append(candidate)

    return particles