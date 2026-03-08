from particle import Particle

def write_static_file(filename: str, particles: list[Particle], L: float):

    with open(filename, "w") as f:

        f.write(f"{len(particles)}\n")
        f.write(f"{L}\n")

        for p in particles:
            f.write(f"{p.radius} {p.property}\n")

def write_dynamic_file(filename: str, particles: list[Particle], t: float = 0.0):

    with open(filename, "w") as f:

        f.write(f"{t}\n")

        for p in particles:
            f.write(f"{p.x} {p.y} {p.vx} {p.vy}\n")

