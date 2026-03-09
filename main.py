import time
import argparse
import random

from generator import generate_particles
from brute_force import brute_force_neighbors, brute_force_neighbors_periodic
from cim import cim_neighbors, cim_neighbors_periodic
from io_utils import write_static_file, write_dynamic_file, write_neighbors_file
from visualizer import plot_particles


def measure_time(function, *args):
    start = time.perf_counter()
    result = function(*args)
    end = time.perf_counter()
    return result, end - start


def normalize_neighbors(neighbors):
    return {pid: sorted(lst) for pid, lst in neighbors.items()}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=20)
    parser.add_argument("--M", type=int, default=10)
    parser.add_argument("--periodic", action="store_true")
    return parser.parse_args()


def main():
    args = parse_arguments()

    N = args.N
    M = args.M
    periodic = args.periodic

    L = 20
    rc = 1
    r_min = 0.23
    r_max = 0.26

    print("N recibido:", N)
    print("M recibido:", M)
    print("Periódico:", periodic)
    print()

    particles = generate_particles(N, L, r_min, r_max)

    write_static_file("static.txt", particles, L)
    write_dynamic_file("dynamic.txt", particles)

    if periodic:
        bf_result, bf_time = measure_time(brute_force_neighbors_periodic, particles, rc, L)
        cim_result, cim_time = measure_time(cim_neighbors_periodic, particles, L, M, rc)
    else:
        bf_result, bf_time = measure_time(brute_force_neighbors, particles, rc)
        cim_result, cim_time = measure_time(cim_neighbors, particles, L, M, rc)

    bf_result = normalize_neighbors(bf_result)
    cim_result = normalize_neighbors(cim_result)

    write_neighbors_file("neighbors_bruteforce.txt", bf_result)
    write_neighbors_file("neighbors_cim.txt", cim_result)

    if bf_result == cim_result:
        print("✔ Lista de vecinos coincide entre Fuerza Bruta y CIM.")
    else:
        print("✖ Listas de vecinos NO coinciden entre Fuerza Bruta y CIM.")

    print()
    print(f"Tiempo brute force: {bf_time:.6f} s")
    print(f"Tiempo CIM:         {cim_time:.6f} s")

    target_id = random.randint(0, N - 1)
    plot_particles(particles, cim_result, target_id, L, rc, "neighbors_plot.png", periodic=periodic)

if __name__ == "__main__":
    main()