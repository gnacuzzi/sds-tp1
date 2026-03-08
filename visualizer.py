import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from particle import Particle


def plot_particles(
    particles,
    neighbors,
    target_id,
    L,
    rc,
    output_file=None,
    periodic=False
):
    fig, ax = plt.subplots(figsize=(8, 8))

    target_neighbors = set(neighbors.get(target_id, []))

    target_particle = None
    for p in particles:
        if p.id == target_id:
            target_particle = p
            break

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
            alpha=0.8
        )

        ax.add_patch(circle)

        ax.text(p.x, p.y, str(p.id), ha="center", va="center", fontsize=8)

    # dibujar radio de interacción
    if target_particle is not None:

        interaction_radius = target_particle.radius + rc

        if periodic:
            shifts = [(dx, dy) for dx in (-L, 0, L) for dy in (-L, 0, L)]
        else:
            shifts = [(0, 0)]

        for dx, dy in shifts:
            interaction_circle = Circle(
                (target_particle.x + dx, target_particle.y + dy),
                interaction_radius,
                edgecolor="orange",
                facecolor="none",
                linestyle="--",
                linewidth=2,
                alpha=0.9 if (dx == 0 and dy == 0) else 0.45
            )

            ax.add_patch(interaction_circle)

    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_aspect("equal")

    ax.set_title(f"Partícula objetivo: {target_id} | Vecinos en verde")

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.grid(True)

    if output_file is not None:
        plt.savefig(output_file, dpi=300, bbox_inches="tight")

    plt.show()