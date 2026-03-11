# Testing

Esta carpeta contiene scripts para **benchmarks reproducibles** del TP.

## Benchmark: tiempo de CIM vs M

Script: `testing/benchmark_cim_m.sh`

### Qué hace

- Corre `./tp1 N M periodic` muchas veces (iteraciones) para una lista de valores de `M`.
- Extrae el número de la línea `CIM time: ... s`.
- Guarda todas las mediciones crudas en `testing/out/cim_times.tsv`.
- Imprime un **resumen** por `M` (mean/std/min/max).

### Comando para ejecutar (con iteraciones como parámetro)

Desde la raíz del repo:

```bash
chmod +x testing/benchmark_cim_m.sh
./testing/benchmark_cim_m.sh -i 200
```

### Opciones útiles

- Cambiar N:

```bash
./testing/benchmark_cim_m.sh -i 200 -N 800
```

- Activar períodico:

```bash
./testing/benchmark_cim_m.sh -i 200 -p 1
```

- Probar solo algunos M:

```bash
./testing/benchmark_cim_m.sh -i 200 -m "13 12 11 10"
```

## Generar gráfico del experimento de M

Para visualizar los resultados del benchmark de CIM y el análisis del valor óptimo de `M`, se puede generar un gráfico utilizando el script de Python incluido en el repositorio.

Ejecutar:

```bash
python3 python/plot_cim_m.py
```

El script lee los datos generados por el benchmark y produce un gráfico con el tiempo de ejecución de CIM en función de `M`.
