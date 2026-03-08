from experiments import (
    experiment_vary_N,
    experiment_vary_M,
    plot_vary_N,
    plot_vary_M
)


def main():
    periodic = False
    repeats = 10

    # Experimento 1: variar N
    N_values = [20, 40, 60, 80, 100]
    M_fixed = 10

    results_N = experiment_vary_N(
        N_values=N_values,
        M=M_fixed,
        repeats=repeats,
        periodic=periodic
    )
    plot_vary_N(results_N, M_fixed, periodic=periodic, log_scale=False)

    # Experimento 2: variar M
    N_fixed = 100
    M_values = [2, 4, 6, 8, 10, 12]

    results_M = experiment_vary_M(
        N=N_fixed,
        M_values=M_values,
        repeats=repeats,
        periodic=periodic
    )
    plot_vary_M(results_M, N_fixed, periodic=periodic, log_scale=False)


if __name__ == "__main__":
    main()