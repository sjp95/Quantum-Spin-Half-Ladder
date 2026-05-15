#!/usr/bin/env python3

import os
import glob
import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Usage:
# python3 thermo_from_eigen.py N [J1] [J2] [hz]
#
# Examples:
# python3 thermo_from_eigen.py 12 1.0 1.0
# python3 thermo_from_eigen.py 12 1.0 1.0 all
# python3 thermo_from_eigen.py 12 1.0 1.0 1.16
# ============================================================

if len(sys.argv) < 2:
    print("Usage: python3 thermo_from_eigen.py N [J1] [J2] [hz]")
    sys.exit(1)

N = int(sys.argv[1])
J1 = int(round(float(sys.argv[2]) * 100)) if len(sys.argv) > 2 else 100
J2 = int(round(float(sys.argv[3]) * 100)) if len(sys.argv) > 3 else 100

hz_filter = None

if len(sys.argv) > 4:
    if sys.argv[4].lower() != "all":
        hz_filter = int(round(float(sys.argv[4]) * 100))

# ============================================================
# Paths
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.normpath(
    os.path.join(base_dir, "Data", "Eigen", "Eigen")
)

if hz_filter is None:
    pattern = f"EigenSpectrum_{N}_{J1}_{J2}_*.h5"
else:
    pattern = f"EigenSpectrum_{N}_{J1}_{J2}_{hz_filter}.h5"

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
# Temperature grid
# ============================================================

Tvals = np.linspace(0.02, 5.0, 300)

# ============================================================
# Plot setup
# ============================================================

figE, axE = plt.subplots(figsize=(8, 6))
figCv, axCv = plt.subplots(figsize=(8, 6))

# ============================================================
# Thermodynamics
# ============================================================

for filepath in file_paths:

    hz = extract_hz(filepath) / 100.0

    with h5py.File(filepath, "r") as f:
        eigenvalues = np.array(f["eigenvalues"][:]).flatten()

    # Numerical stability
    E0 = np.min(eigenvalues)
    energies = eigenvalues - E0

    avgE = []
    Cv = []

    for T in Tvals:
        beta = 1.0 / T

        weights = np.exp(-beta * energies)
        Z = np.sum(weights)

        Eavg_shifted = np.sum(energies * weights) / Z
        E2avg_shifted = np.sum((energies ** 2) * weights) / Z

        Eavg = Eavg_shifted + E0
        CvT = (E2avg_shifted - Eavg_shifted ** 2) / (T * T)

        avgE.append(Eavg)
        Cv.append(CvT)

    avgE = np.array(avgE)
    Cv = np.array(Cv)

    axE.plot(Tvals, avgE, label=fr"$h_z={hz:.2f}$")
    axCv.plot(Tvals, Cv, label=fr"$h_z={hz:.2f}$")

    print(f"Processed hz = {hz:.2f}")

# ============================================================
# Labels
# ============================================================

axE.set_xlabel(r"$T$")
axE.set_ylabel(r"$\langle E \rangle$")
axE.set_title("Average Energy vs Temperature")
axE.legend()
axE.grid(True)

axCv.set_xlabel(r"$T$")
axCv.set_ylabel(r"$C_v$")
axCv.set_title(r"Specific Heat $C_v$ vs Temperature")
axCv.legend()
axCv.grid(True)

# ============================================================
# Save
# ============================================================

output_dir = os.path.join(base_dir, "Plots")
os.makedirs(output_dir, exist_ok=True)

figE.tight_layout()
figCv.tight_layout()

suffix = "all" if hz_filter is None else f"hz_{hz_filter}"

figE.savefig(
    os.path.join(
        output_dir,
        f"Energy_vs_T_N{N}_J1{J1}_J2{J2}_{suffix}.png"
    ),
    dpi=300
)

figCv.savefig(
    os.path.join(
        output_dir,
        f"Cv_vs_T_N{N}_J1{J1}_J2{J2}_{suffix}.png"
    ),
    dpi=300
)

plt.show()