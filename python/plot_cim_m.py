import csv
import math
import os
from collections import defaultdict

import matplotlib.pyplot as plt


INPUT_FILE = "testing/out/cim_times.tsv"
OUTPUT_PLOT = "output/cim_time_vs_M.png"


def mean(values):
    return sum(values) / len(values)


def stddev(values):
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)


def read_tsv(filename):
    metadata = {}
    grouped = defaultdict(list)

    with open(filename, "r") as f:
        lines = []
        for line in f:
            if line.startswith("#"):
                key, value = line[1:].strip().split("=")
                metadata[key] = value
            else:
                lines.append(line)

    reader = csv.DictReader(lines, delimiter="\t")

    for row in reader:
        M = int(row["M"])
        t = float(row["cim_time_seconds"])
        grouped[M].append(t)

    return metadata, grouped


def summarize(grouped):
    summary = []

    for M in sorted(grouped.keys()):
        values = grouped[M]
        summary.append(
            {
                "M": M,
                "count": len(values),
                "mean": mean(values),
                "std": stddev(values),
                "min": min(values),
                "max": max(values),
            }
        )

    return summary


def print_summary(summary):
    print("M\tcount\tmean_s\tstd_s\tmin_s\tmax_s")
    for row in summary:
        print(
            f"{row['M']}\t"
            f"{row['count']}\t"
            f"{row['mean']:.8f}\t"
            f"{row['std']:.8f}\t"
            f"{row['min']:.8f}\t"
            f"{row['max']:.8f}"
        )


def plot_summary(summary, metadata, log_scale=False):
    os.makedirs("output", exist_ok=True)

    M_values = [row["M"] for row in summary]
    means = [row["mean"] for row in summary]
    stds = [row["std"] for row in summary]

    plt.figure(figsize=(8, 6))
    plt.errorbar(
        M_values,
        means,
        yerr=stds,
        marker="o",
        capsize=4,
        label="CIM"
    )

    plt.xlabel("M")
    plt.ylabel("Execution time (s)")
    plt.title(
        f"CIM execution time vs M\n"
        f"N={metadata.get('N')} | iters={metadata.get('iters')}"
    )
    plt.grid(True)
    plt.legend()

    if log_scale:
        plt.yscale("log")

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT, dpi=300)
    plt.close()


def main():
    metadata, grouped = read_tsv(INPUT_FILE)    
    summary = summarize(grouped)

    print_summary(summary)
    plot_summary(summary, metadata, log_scale=False)

    print()
    print(f"Plot written to: {OUTPUT_PLOT}")


if __name__ == "__main__":
    main()