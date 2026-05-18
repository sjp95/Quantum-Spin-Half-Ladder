import os
import glob
import sys
import h5py
import numpy as np

# ============================================================
# Usage:
# python3 Eh_hdf5.py N [J1] [J2]
#
# Example:
# python3 Eh_hdf5.py 4 1.0 1.0
# ============================================================

if len(sys.argv) < 2:
    print("Usage: python3 Eh_hdf5.py N [J1] [J2]")
    sys.exit(1)

N = int(sys.argv[1])

J1 = int(float(sys.argv[2]) * 100) if len(sys.argv) > 2 else 100
J2 = int(float(sys.argv[3]) * 100) if len(sys.argv) > 3 else 100
hx = int(float(sys.argv[4]) * 100) if len(sys.argv) > 4 else 100
hy = int(float(sys.argv[5]) * 100) if len(sys.argv) > 5 else 100

# ============================================================
# Paths
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.normpath(
    os.path.join(base_dir, "..", "Data", "Eigen", "Eigen")
)

pattern = f"EigenSpectrum_{N}_{J1}_{J2}_{hx}_{hy}_*.h5"

file_paths = glob.glob(os.path.join(data_dir, pattern))

if not file_paths:
    print(f"No files found for pattern: {pattern}")
    sys.exit(1)

# ============================================================
# Extract hz from filename
# ============================================================

def extract_hz(filepath):
    name = os.path.basename(filepath)
    parts = name.replace(".h5", "").split("_")
    return int(parts[-1])

file_paths.sort(key=extract_hz)

# ============================================================
# Output paths
# ============================================================

combined_dir = os.path.join(base_dir, "..", "Data", "Eigen", "Combined")
derivative_dir = os.path.join(base_dir, "..", "Data", "Eigen", "Derivatives")

os.makedirs(combined_dir, exist_ok=True)
os.makedirs(derivative_dir, exist_ok=True)

combined_output = os.path.join(
    combined_dir,
    f"combined_energy_data_{J1}_{J2}_{hx}_{hy}_{N}.txt"
)

derivative_output = os.path.join(
    derivative_dir,
    f"second_derivative_energy_data_{J1}_{J2}_{hx}_{hy}_{N}.txt"
)

# ============================================================
# Read HDF5
# ============================================================

hz_values = []
energy_values = []

with open(combined_output, "w") as outfile:

    for filepath in file_paths:
        try:
            hz = extract_hz(filepath) / 100.0

            with h5py.File(filepath, "r") as f:
                eigenvalues = f["eigenvalues"][:]
                ground_energy = float(eigenvalues.flatten()[0])

            hz_values.append(hz)
            energy_values.append(ground_energy)

            outfile.write(
                f"{hx/100.0} {hy/100.0} {hz} {J1/100.0} {J2/100.0} {ground_energy}\n"
            )

            print(f"Processed: {os.path.basename(filepath)}")

        except Exception as e:
            print(f"Error reading {filepath}: {e}")

print(f"\nCombined data written to:\n{combined_output}")

# ============================================================
# Second derivative
# ============================================================

hz_values = np.array(hz_values)
energy_values = np.array(energy_values)

def second_derivative_4th_order(x, y):
    n = len(x)

    if n < 5:
        return np.gradient(np.gradient(y, x), x)

    dx = np.diff(x)

    if not np.allclose(dx, dx[0]):
        return np.gradient(np.gradient(y, x), x)

    h = dx[0]
    d2 = np.zeros(n)

    for i in range(2, n - 2):
        d2[i] = (
            -y[i + 2]
            + 16 * y[i + 1]
            - 30 * y[i]
            + 16 * y[i - 1]
            - y[i - 2]
        ) / (12 * h * h)

    d2[1] = (y[0] - 2 * y[1] + y[2]) / (h * h)
    d2[-2] = (y[-3] - 2 * y[-2] + y[-1]) / (h * h)

    d2[0] = (2 * y[0] - 5 * y[1] + 4 * y[2] - y[3]) / (h * h)
    d2[-1] = (2 * y[-1] - 5 * y[-2] + 4 * y[-3] - y[-4]) / (h * h)

    return d2

second_derivative = second_derivative_4th_order(hz_values, energy_values)

# ============================================================
# Write derivative data
# ============================================================

with open(derivative_output, "w") as outfile:
    for hz, d2e in zip(hz_values, second_derivative):
        outfile.write(
            f"{hx/100.0} {hy/100.0} {hz} {J1/100.0} {J2/100.0} {d2e}\n"
        )

print(f"Second derivative data written to:\n{derivative_output}")