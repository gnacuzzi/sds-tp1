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


def write_neighbors_file(filename, neighbors):
    """
    Writes neighbor list to file in the format:

    [particle_id neighbor1 neighbor2 neighbor3 ...]
    """

    with open(filename, "w") as f:
        for pid in sorted(neighbors.keys()):
            neighs = sorted(neighbors[pid])

            line = f"[{pid}"

            if neighs:
                line += " " + " ".join(str(n) for n in neighs)

            line += "]"

            f.write(line + "\n")

