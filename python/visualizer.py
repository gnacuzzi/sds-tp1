import argparse
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


@dataclass
class Particle:
    id: int
    x: float
    y: float
    radius: float
    property: float = 0.0
    vx: float = 0.0
    vy: float = 0.0


def read_static_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    L = float(lines[1])

    radii = []
    properties = []

    for i in range(n):
        radius, prop = map(float, lines[2 + i].split())
        radii.append(radius)
        properties.append(prop)

    return n, L, radii, properties


def read_dynamic_file(filename, n):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    t = float(lines[0])

    positions = []
    velocities = []

    for i in range(n):
        x, y, vx, vy = map(float, lines[1 + i].split())
        positions.append((x, y))
        velocities.append((vx, vy))

    return t, positions, velocities


def read_neighbors_file(filename):
    neighbors = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            line = line.strip("[]")
            parts = line.split()

            pid = int(parts[0])
            neighs = list(map(int, parts[1:])) if len(parts) > 1 else []

            neighbors[pid] = neighs

    return neighbors


def load_particles(static_file, dynamic_file):
    n, L, radii, properties = read_static_file(static_file)
    _, positions, velocities = read_dynamic_file(dynamic_file, n)

    particles = []
    for i in range(n):
        x, y = positions[i]
        vx, vy = velocities[i]

        particles.append(
            Particle(
                id=i,
                x=x,
                y=y,
                radius=radii[i],
                property=properties[i],
                vx=vx,
                vy=vy,
            )
        )

    return particles, L


def draw_grid(ax, L, M):
    cell_size = L / M

    for i in range(M + 1):
        x = i * cell_size
        y = i * cell_size

        ax.plot([x, x], [0, L], linestyle="--", linewidth=0.8, alpha=0.5)
        ax.plot([0, L], [y, y], linestyle="--", linewidth=0.8, alpha=0.5)


def plot_particles(
    particles,
    neighbors,
    target_id,
    L,
    M,
    rc,
    output_file,
    periodic=False
):
    fig, ax = plt.subplots(figsize=(8, 8))

    target_neighbors = set(neighbors.get(target_id, []))
    target_particle = next((p for p in particles if p.id == target_id), None)

    draw_grid(ax, L, M)

    # dibujar partículas
    for p in particles:
        if p.id == target_id:
            color = "red"
        elif p.id in target_neighbors:
            color = "green"
        else:
            color = "lightblue"

        circle = Circle(
            (p.x, p.y),
            p.radius,
            edgecolor="black",
            facecolor=color,
            alpha=0.85,
            linewidth=0.25,
            zorder=3
        )
        ax.add_patch(circle)

        ax.text(
            p.x, p.y, str(p.id),
            ha="center", va="center",
            fontsize=7,
            zorder=4
        )

    # dibujar círculo de interacción
    if target_particle is not None:
        interaction_radius = target_particle.radius + rc

        def add_interaction_circle(cx, cy, alpha=0.95):
            interaction_circle = Circle(
                (cx, cy),
                interaction_radius,
                edgecolor="orange",
                facecolor="none",
                linestyle="--",
                linewidth=0.25,
                alpha=alpha,
                zorder=10
            )
            ax.add_patch(interaction_circle)

        # círculo principal
        add_interaction_circle(target_particle.x, target_particle.y, alpha=0.95)

        if periodic:
            x = target_particle.x
            y = target_particle.y
            r = interaction_radius

            # wrap horizontal
            if x + r > L:
                add_interaction_circle(x - L, y, alpha=0.95)
            if x - r < 0:
                add_interaction_circle(x + L, y, alpha=0.95)

            # wrap vertical
            if y + r > L:
                add_interaction_circle(x, y - L, alpha=0.95)
            if y - r < 0:
                add_interaction_circle(x, y + L, alpha=0.95)

            # wrap en esquinas
            if x + r > L and y + r > L:
                add_interaction_circle(x - L, y - L, alpha=0.95)
            if x + r > L and y - r < 0:
                add_interaction_circle(x - L, y + L, alpha=0.95)
            if x - r < 0 and y + r > L:
                add_interaction_circle(x + L, y - L, alpha=0.95)
            if x - r < 0 and y - r < 0:
                add_interaction_circle(x + L, y + L, alpha=0.95)

    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_aspect("equal")
    ax.set_title(f"Target particle: {target_id} | Neighbors in green")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(False)

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(description="Particle system visualizer")
    parser.add_argument("--target", type=int, required=True)
    parser.add_argument("--M", type=int, required=True)
    parser.add_argument("--rc", type=float, default=1.0)
    parser.add_argument("--periodic", action="store_true")
    parser.add_argument("--output", default="output/neighbors_plot.png")
    return parser.parse_args()


def main():
    args = parse_args()

    particles, L = load_particles("data/static.txt", "data/dynamic.txt")
    neighbors = read_neighbors_file("data/neighbors_cim.txt")

    if args.target < 0 or args.target >= len(particles):
        raise ValueError(f"Invalid target particle id: {args.target}")

    plot_particles(
        particles=particles,
        neighbors=neighbors,
        target_id=args.target,
        L=L,
        M=args.M,
        rc=args.rc,
        output_file=args.output,
        periodic=args.periodic
    )


if __name__ == "__main__":
    main()