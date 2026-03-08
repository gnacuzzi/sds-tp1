import time
import statistics
import matplotlib.pyplot as plt

from generator import generate_particles
from brute_force import brute_force_neighbors, brute_force_neighbors_periodic
from cim import cim_neighbors, cim_neighbors_periodic


def measure_time(function, *args):
    start = time.perf_counter()
    result = function(*args)
    end = time.perf_counter()
    return result, end - start


def mean_and_std(values):
    mean = statistics.mean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    return mean, std


def experiment_vary_N(
    N_values,
    M,
    repeats,
    L=20,
    rc=1,
    r_min=0.23,
    r_max=0.26,
    periodic=False
):
    results = []

    for N in N_values:
        bf_times = []
        cim_times = []

        print(f"Probando N = {N}")

        for _ in range(repeats):
            particles = generate_particles(N, L, r_min, r_max)

            if periodic:
                _, bf_time = measure_time(brute_force_neighbors_periodic, particles, rc, L)
                _, cim_time = measure_time(cim_neighbors_periodic, particles, L, M, rc)
            else:
                _, bf_time = measure_time(brute_force_neighbors, particles, rc)
                _, cim_time = measure_time(cim_neighbors, particles, L, M, rc)

            bf_times.append(bf_time)
            cim_times.append(cim_time)

        bf_mean, bf_std = mean_and_std(bf_times)
        cim_mean, cim_std = mean_and_std(cim_times)

        results.append({
            "N": N,
            "bf_mean": bf_mean,
            "bf_std": bf_std,
            "cim_mean": cim_mean,
            "cim_std": cim_std
        })

    return results


def experiment_vary_M(
    N,
    M_values,
    repeats,
    L=20,
    rc=1,
    r_min=0.23,
    r_max=0.26,
    periodic=False
):
    results = []

    for M in M_values:
        bf_times = []
        cim_times = []

        print(f"Probando M = {M}")

        for _ in range(repeats):
            particles = generate_particles(N, L, r_min, r_max)

            if periodic:
                _, bf_time = measure_time(brute_force_neighbors_periodic, particles, rc, L)
                _, cim_time = measure_time(cim_neighbors_periodic, particles, L, M, rc)
            else:
                _, bf_time = measure_time(brute_force_neighbors, particles, rc)
                _, cim_time = measure_time(cim_neighbors, particles, L, M, rc)

            bf_times.append(bf_time)
            cim_times.append(cim_time)

        bf_mean, bf_std = mean_and_std(bf_times)
        cim_mean, cim_std = mean_and_std(cim_times)

        results.append({
            "M": M,
            "bf_mean": bf_mean,
            "bf_std": bf_std,
            "cim_mean": cim_mean,
            "cim_std": cim_std
        })

    return results


def plot_vary_N(results, M, periodic=False, log_scale=False):
    N_values = [r["N"] for r in results]

    bf_means = [r["bf_mean"] for r in results]
    bf_stds = [r["bf_std"] for r in results]

    cim_means = [r["cim_mean"] for r in results]
    cim_stds = [r["cim_std"] for r in results]

    plt.figure(figsize=(8, 6))

    plt.errorbar(N_values, bf_means, yerr=bf_stds, marker="o", capsize=4, label="Brute Force")
    plt.errorbar(N_values, cim_means, yerr=cim_stds, marker="o", capsize=4, label="CIM")

    plt.xlabel("N")
    plt.ylabel("Tiempo (s)")
    plt.title(f"Tiempo vs N (M={M}, periodic={periodic})")
    plt.legend()
    plt.grid(True)

    if log_scale:
        plt.yscale("log")

    plt.tight_layout()
    plt.savefig("experiment_vary_N.png", dpi=300)
    plt.show()


def plot_vary_M(results, N, periodic=False, log_scale=False):
    M_values = [r["M"] for r in results]

    bf_means = [r["bf_mean"] for r in results]
    bf_stds = [r["bf_std"] for r in results]

    cim_means = [r["cim_mean"] for r in results]
    cim_stds = [r["cim_std"] for r in results]

    plt.figure(figsize=(8, 6))

    plt.errorbar(M_values, bf_means, yerr=bf_stds, marker="o", capsize=4, label="Brute Force")
    plt.errorbar(M_values, cim_means, yerr=cim_stds, marker="o", capsize=4, label="CIM")

    plt.xlabel("M")
    plt.ylabel("Tiempo (s)")
    plt.title(f"Tiempo vs M (N={N}, periodic={periodic})")
    plt.legend()
    plt.grid(True)

    if log_scale:
        plt.yscale("log")

    plt.tight_layout()
    plt.savefig("experiment_vary_M.png", dpi=300)
    plt.show()