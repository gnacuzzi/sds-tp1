import argparse
import csv
import math
import os
import numpy as np
from collections import defaultdict
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

def model_n2(x, a):
    return a * x**2

def model_n(x, a):
    return a * x

def model_n2_offset(x, a, b):
    return a * x**2 + b

def model_n_offset(x, a, b):
    return a * x + b

def mean(values):
    return sum(values) / len(values)


def stddev(values):
    if len(values) < 2:
        return 0.0

    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)


def read_performance_csv(filename):
    metadata = {}
    rows = []

    with open(filename, "r") as f:
        data_lines = []

        for line in f:
            if line.startswith("#"):
                content = line[1:].strip()
                if "=" in content:
                    key, value = content.split("=", 1)
                    metadata[key.strip()] = value.strip()
            else:
                if line.startswith("study"):
                    data_lines.append(line)
                elif not line.startswith("#"):
                    data_lines.append(line)

    reader = csv.DictReader(data_lines)

    for row in reader:

        # saltear líneas basura o headers repetidos
        if not row["N"].isdigit():
            continue

        rows.append(
            {
                "study": row["study"],
                "N": int(row["N"]),
                "M": int(row["M"]),
                "method": row["method"],
                "run": int(row["run"]),
                "time_seconds": float(row["time_seconds"]),
            }
        )

    return metadata, rows

def build_title_vary_n(metadata):
    return (
        "Execution Time vs N\n"
        f"L={metadata.get('L')} | rc={metadata.get('rc')} | "
        f"ri~U[{metadata.get('r_min')}, {metadata.get('r_max')}] | "
        f"M fixed={metadata.get('vary_N_M_fixed')}"
    )


def build_title_vary_m(metadata):
    return (
        "Execution Time vs M\n"
        f"L={metadata.get('L')} | rc={metadata.get('rc')} | "
        f"ri~U[{metadata.get('r_min')}, {metadata.get('r_max')}] | "
        f"N fixed={metadata.get('vary_M_N_fixed')}"
    )


def group_statistics(rows, study_name, x_field):
    grouped = defaultdict(list)

    for row in rows:
        if row["study"] != study_name:
            continue

        key = (row[x_field], row["method"])
        grouped[key].append(row["time_seconds"])

    stats = defaultdict(dict)

    for (x_value, method), times in grouped.items():
        stats[method][x_value] = {
            "mean": mean(times),
            "std": stddev(times),
        }

    return stats


def plot_study(stats, x_label, title, output_file, log_scale=False, show_ON=False):
    plt.figure(figsize=(10, 6))

    methods = ["brute_force", "cim"]
    labels = {
        "brute_force": "Brute Force",
        "cim": "CIM",
    }

    for method in methods:
        if method not in stats:
            continue

        x_values = sorted(stats[method].keys())
        means = [stats[method][x]["mean"] for x in x_values]
        stds = [stats[method][x]["std"] for x in x_values]

        plt.errorbar(
            x_values,
            means,
            yerr=stds,
            marker="o",
            capsize=4,
            label=labels[method],
        )

    if show_ON:
        if "brute_force" in stats:
            x_bf = np.array(sorted(stats["brute_force"].keys()), dtype=float)
            y_bf = np.array([stats["brute_force"][x]["mean"] for x in x_bf], dtype=float)

            popt_bf, _ = curve_fit(model_n2, x_bf, y_bf)
            a_bf = popt_bf[0]

            x_fit = np.linspace(min(x_bf), max(x_bf), 300)
            y_fit_bf = model_n2(x_fit, a_bf)

            plt.plot(x_fit, y_fit_bf, label=f"Fit Brute Force ≈ {a_bf:.2e}·N²")

        if "cim" in stats:
            x_cim = np.array(sorted(stats["cim"].keys()), dtype=float)
            y_cim = np.array([stats["cim"][x]["mean"] for x in x_cim], dtype=float)

            popt_cim, _ = curve_fit(model_n, x_cim, y_cim)
            a_cim = popt_cim[0]

            x_fit = np.linspace(min(x_cim), max(x_cim), 300)
            y_fit_cim = model_n(x_fit, a_cim)

            plt.plot(x_fit, y_fit_cim, label=f"Fit CIM ≈ {a_cim:.2e}·N")

    plt.xlabel(x_label)
    plt.ylabel("Time (s)")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    if log_scale:
        plt.yscale("log")

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

def arg_parser():
    parser = argparse.ArgumentParser(description="Particle preformanze analyzer")
    parser.add_argument("--sON", action="store_true")
    return parser.parse_args()

def main():
    args = arg_parser()

    input_file = "data/performance.csv"
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    metadata, rows = read_performance_csv(input_file)

    # Study 1: vary N
    stats_vary_n = group_statistics(rows, "vary_N", "N")
    plot_study(
        stats=stats_vary_n,
        x_label="N",
        title=build_title_vary_n(metadata),
        output_file=os.path.join(output_dir, "experiment_vary_N.png"),
        log_scale=False,
        show_ON=args.sON
    )

    # Study 2: vary M
    stats_vary_m = group_statistics(rows, "vary_M", "M")
    plot_study(
        stats=stats_vary_m,
        x_label="M",
        title=build_title_vary_m(metadata),
        output_file=os.path.join(output_dir, "experiment_vary_M.png"),
        log_scale=False,
        show_ON=False
    )

    print("Plots generated:")
    print(" - output/experiment_vary_N.png")
    print(" - output/experiment_vary_M.png")


if __name__ == "__main__":
    main()