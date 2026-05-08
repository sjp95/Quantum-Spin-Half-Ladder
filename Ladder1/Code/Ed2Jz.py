import os
import glob
import sys
import numpy as np

# Parameters
if len(sys.argv) < 2:
    print("Usage: EJz.py N [hz] [Jx]")
    sys.exit(1)

N = int(sys.argv[1])
hz = int(float(sys.argv[2]) * 100) if len(sys.argv) > 2 else 0
Jx = int(float(sys.argv[3]) * 100) if len(sys.argv) > 3 else 100

# Read all matching files
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Energy"))
pattern = f"E_{N}_{Jx}_*_{hz}.dat"
file_paths = glob.glob(os.path.join(data_dir, pattern))
if not file_paths:
    file_paths = glob.glob(os.path.join(base_dir, "..", "Data", "Energy", pattern))
if not file_paths:
    print(f"No files found for pattern: {os.path.join(data_dir, pattern)}")

# Sort files to process in order
file_paths.sort()

# Read all data lines and sort by Kitayev.h
all_data_lines = []

for file_path in file_paths:
    try:
        with open(file_path, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                first_tok = line.split()[0]
                try:
                    float(first_tok)
                except ValueError:
                    continue
                all_data_lines.append(line)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Sort by the first column (Kitayev.h)
all_data_lines.sort(key=lambda x: float(x.split()[0]))

# Write results to a single output file
output_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Energy", "Combined"))
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"combined_energy_data_{Jx}_{hz}_{N}.txt")

with open(output_path, "w") as outfile:
    for line in all_data_lines:
        outfile.write(line + "\n")

print(f"Data successfully combined into combined_energy_data_{Jx}_{hz}_{N}.txt")

# Compute second derivative of energy with respect to Jz
# Parse data: Jz (first column) and energy (last column)
jz_values = []
energy_values = []

for line in all_data_lines:
    parts = line.split()
    jz_values.append(float(parts[0]))
    energy_values.append(float(parts[-1]))

jz_values = np.array(jz_values)
energy_values = np.array(energy_values)


def second_derivative_4th_order(x, y):
    """Return d²y/dx² using a 4th-order finite-difference stencil."""
    n = len(x)
    if n < 5:
        return np.gradient(np.gradient(y, x), x)

    dx = np.diff(x)
    if not np.allclose(dx, dx[0]):
        return np.gradient(np.gradient(y, x), x)

    h = dx[0]
    d2 = np.zeros(n, dtype=float)

    # 4th-order central stencil for interior points
    for i in range(2, n - 2):
        d2[i] = (-y[i + 2] + 16 * y[i + 1] - 30 * y[i] + 16 * y[i - 1] - y[i - 2]) / (12 * h * h)

    # Edge points: 2nd-order fallback
    if n >= 5:
        d2[1] = (y[0] - 2 * y[1] + y[2]) / (h**2)
        d2[-2] = (y[-3] - 2 * y[-2] + y[-1]) / (h**2)
        d2[0] = (2 * y[0] - 5 * y[1] + 4 * y[2] - y[3]) / (h**2)
        d2[-1] = (2 * y[-1] - 5 * y[-2] + 4 * y[-3] - y[-4]) / (h**2)
    else:
        d2[0] = (y[0] - 2 * y[1] + y[2]) / (h * h)
        d2[1] = (y[0] - 2 * y[1] + y[2]) / (h * h)
        d2[-2] = (y[-3] - 2 * y[-2] + y[-1]) / (h * h)
        d2[-1] = (y[-3] - 2 * y[-2] + y[-1]) / (h * h)

    return d2


# Compute second derivative (d²E/dJz²)
second_derivative = second_derivative_4th_order(jz_values, energy_values)

# Write second derivative to output file
derivative_output_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Energy", "Derivatives"))
os.makedirs(derivative_output_dir, exist_ok=True)
derivative_output_path = os.path.join(derivative_output_dir, f"second_derivative_energy_data_{Jx}_{hz}_{N}.txt")

with open(derivative_output_path, "w") as outfile:
    for jz, d2e in zip(jz_values, second_derivative):
        outfile.write(f"{jz}\t{Jx / 100.0}\t{hz / 100.0}\t{d2e}\n")

print(f"Second derivative data written to second_derivative_energy_data_{Jx}_{hz}_{N}.txt")
