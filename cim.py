from particle import Particle
from geometry import are_neighbors, are_neighbors_periodic


def create_grid(M: int) -> list[list[list[Particle]]]:
    return [[[] for _ in range(M)] for _ in range(M)]


def get_cell_indices(particle: Particle, cell_size: float, M: int) -> tuple[int, int]:
    cx = int(particle.x / cell_size)
    cy = int(particle.y / cell_size)

    if cx >= M:
        cx = M - 1
    if cy >= M:
        cy = M - 1

    return cx, cy


def populate_grid(particles: list[Particle], L: float, M: int) -> list[list[list[Particle]]]:
    grid = create_grid(M)
    cell_size = L / M

    for p in particles:
        cx, cy = get_cell_indices(p, cell_size, M)
        grid[cx][cy].append(p)

    return grid


def neighbor_offsets() -> list[tuple[int, int]]:
    return [
        (0, 0),   # misma celda
        (1, 0),   # derecha
        (0, 1),   # arriba
        (1, 1),   # diagonal arriba derecha
        (-1, 1),  # diagonal arriba izquierda
    ]


def cim_neighbors(particles: list[Particle], L: float, M: int, rc: float) -> dict[int, list[int]]:
    neighbors = {p.id: [] for p in particles}
    grid = populate_grid(particles, L, M)

    for cx in range(M):
        for cy in range(M):
            current_cell = grid[cx][cy]

            for dx, dy in neighbor_offsets():
                nx = cx + dx
                ny = cy + dy

                if nx < 0 or nx >= M or ny < 0 or ny >= M:
                    continue

                other_cell = grid[nx][ny]

                if dx == 0 and dy == 0:
                    for i in range(len(current_cell)):
                        for j in range(i + 1, len(current_cell)):
                            p1 = current_cell[i]
                            p2 = current_cell[j]

                            if are_neighbors(p1, p2, rc):
                                neighbors[p1.id].append(p2.id)
                                neighbors[p2.id].append(p1.id)

                else:
                    for p1 in current_cell:
                        for p2 in other_cell:
                            if are_neighbors(p1, p2, rc):
                                neighbors[p1.id].append(p2.id)
                                neighbors[p2.id].append(p1.id)

    return neighbors


def cim_neighbors_periodic(
    particles: list[Particle], L: float, M: int, rc: float
) -> dict[int, list[int]]:
    neighbors = {p.id: [] for p in particles}
    grid = populate_grid(particles, L, M)

    for cx in range(M):
        for cy in range(M):
            current_cell = grid[cx][cy]

            for dx, dy in neighbor_offsets():
                nx = (cx + dx) % M
                ny = (cy + dy) % M

                other_cell = grid[nx][ny]

                if dx == 0 and dy == 0:
                    for i in range(len(current_cell)):
                        for j in range(i + 1, len(current_cell)):
                            p1 = current_cell[i]
                            p2 = current_cell[j]

                            if are_neighbors_periodic(p1, p2, rc, L):
                                neighbors[p1.id].append(p2.id)
                                neighbors[p2.id].append(p1.id)

                else:
                    for p1 in current_cell:
                        for p2 in other_cell:
                            if are_neighbors_periodic(p1, p2, rc, L):
                                neighbors[p1.id].append(p2.id)
                                neighbors[p2.id].append(p1.id)

    return neighbors