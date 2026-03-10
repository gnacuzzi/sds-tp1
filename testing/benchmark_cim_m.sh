#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# benchmark_cim_m.sh
# -----------------------------------------------------------------------------
# Corre el ejecutable `tp1` muchas veces para varios valores de M y mide
# el tiempo del algoritmo CIM (la línea "CIM time: ... s" que imprime el programa).
#
# - Guarda todas las mediciones crudas en un TSV (tab-separated values).
# - Imprime al final un resumen por cada M: cantidad de corridas, media, desvío,
#   mínimo y máximo.
#
# Uso (desde la raíz del repo):
#   ./testing/benchmark_cim_m.sh -i 200
#
# Parámetros (opcionales):
#   -i <iters>     cantidad de iteraciones por M (default: 30)
#   -N <N>         cantidad de partículas (default: 800)
#   -p <0|1>       0 = paredes, 1 = períodico (default: 0)
#   -m "<lista>"   lista de M separados por espacios (default: "13 12 11 10 9 8 7 6 5 4")
#
# Ejemplo:
#   ./testing/benchmark_cim_m.sh -i 200 -N 800 -p 0 -m "13 12 11 10"
# -----------------------------------------------------------------------------

usage() {
  cat <<'EOF'
Usage: ./testing/benchmark_cim_m.sh [-i iters] [-N particles] [-p 0|1] [-m "M1 M2 ..."]

Runs ./tp1 many times and summarizes CIM time per M.
EOF
}

# Defaults (si el usuario no pasa flags).
ITERS=30
N=800
PERIODIC=0
M_LIST="13 12 11 10 9 8 7 6 5 4"

# Parseo simple de flags con getopts.
while getopts ":i:N:p:m:h" opt; do
  case "$opt" in
    i) ITERS="$OPTARG" ;;
    N) N="$OPTARG" ;;
    p) PERIODIC="$OPTARG" ;;
    m) M_LIST="$OPTARG" ;;
    h) usage; exit 0 ;;
    \?) echo "Unknown option: -$OPTARG" >&2; usage; exit 2 ;;
    :)  echo "Missing argument for -$OPTARG" >&2; usage; exit 2 ;;
  esac
done

# Validaciones básicas de entrada.
if [[ "$ITERS" -le 0 ]]; then
  echo "Error: -i must be > 0" >&2
  exit 2
fi
if [[ "$N" -le 0 ]]; then
  echo "Error: -N must be > 0" >&2
  exit 2
fi
if [[ "$PERIODIC" != "0" && "$PERIODIC" != "1" ]]; then
  echo "Error: -p must be 0 or 1" >&2
  exit 2
fi

# Nos movemos a la raíz del repo, independientemente de desde dónde se ejecuta.
# Esto permite invocar ./tp1 con path relativo consistente.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Output: carpeta y archivo de datos crudos.
OUT_DIR="testing/out"
RAW_TSV="${OUT_DIR}/cim_times.tsv"
mkdir -p "$OUT_DIR"

# Escribimos header para que sea auto-documentado.
echo -e "M\trun\tcim_time_seconds" > "$RAW_TSV"

# -----------------------------------------------------------------------------
# Loop principal del benchmark
# -----------------------------------------------------------------------------
#
# Para cada M en la lista:
#   - corremos ITERS veces: ./tp1 N M PERIODIC
#   - "parseamos" el tiempo de CIM desde stdout
#   - guardamos M, run, tiempo a RAW_TSV
#
# La parte más "difícil" suele ser extraer el número:
# El programa imprime una línea así:
#   CIM time:         0.00045029 s
#
# Entonces usamos awk con un patrón:
#   /CIM time/  -> matchea la línea
#   {print $3}  -> en esa línea, el 3er "campo" es el número (0.00045029)
# -----------------------------------------------------------------------------

for M in $M_LIST; do
  for run in $(seq 1 "$ITERS"); do
    cim_time="$(
      ./tp1 "$N" "$M" "$PERIODIC" \
        | awk '/CIM time/ { print $3 }'
    )"
    echo -e "${M}\t${run}\t${cim_time}" >> "$RAW_TSV"
  done
done

# -----------------------------------------------------------------------------
# Resumen estadístico por M (sin depender de Python)
# -----------------------------------------------------------------------------
#
# Leemos el TSV y calculamos por cada M:
#   - count
#   - mean
#   - stddev (muestral)
#   - min / max
#
# Usamos el algoritmo online de Welford para mean/varianza de forma estable.
# -----------------------------------------------------------------------------

awk -F'\t' '
  NR==1 { next } # salteo header
  {
    m = $1
    x = $3 + 0.0

    # count
    n[m]++

    # min/max
    if (!(m in min) || x < min[m]) min[m] = x
    if (!(m in max) || x > max[m]) max[m] = x

    # Welford: update mean and M2
    delta = x - mean[m]
    mean[m] += delta / n[m]
    delta2 = x - mean[m]
    M2[m] += delta * delta2
  }
  END {
    # Header del resumen.
    printf("Benchmark CIM (N=%d, periodic=%d, iters=%d per M)\n", '"$N"', '"$PERIODIC"', '"$ITERS"')
    print("M\tcount\tmean_s\tstd_s\tmin_s\tmax_s")

    # Imprimimos los M en el mismo orden que se pasó por -m (más lindo para leer).
    split("'"$M_LIST"'", order, " ")
    for (i = 1; i <= length(order); i++) {
      m = order[i]
      if (m == "") continue
      if (!(m in n)) continue

      # stddev muestral: sqrt(M2/(n-1)) si n>1
      if (n[m] > 1) std = sqrt(M2[m] / (n[m] - 1))
      else std = 0.0

      printf("%s\t%d\t%.8f\t%.8f\t%.8f\t%.8f\n", m, n[m], mean[m], std, min[m], max[m])
    }
  }
' "$RAW_TSV"

echo
echo "Raw measurements written to: $RAW_TSV"

