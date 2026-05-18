import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Usage:
# python3 plot_energy.py N [J1] [J2] [hx] [hy]
# ============================================================

if len(sys.argv) < 2:
    print("Usage: python3 plot_energy.py N [J1] [J2]")
    sys.exit(1)

N = int(sys.argv[1])

J1 = int(float(sys.argv[2]) * 100) if len(sys.argv) > 2 else 100
J2 = int(float(sys.argv[3]) * 100) if len(sys.argv) > 3 else 100
hx = int(float(sys.argv[4]) * 100) if len(sys.argv) > 4 else 100
hy = int(float(sys.argv[5]) * 100) if len(sys.argv) > 5 else 100

base_dir = os.path.dirname(os.path.abspath(__file__))

energy_file = os.path.join(
    base_dir,
    "Data",
    "Eigen",
    "Combined",
    f"combined_energy_data_{J1}_{J2}_{hx}_{hy}_{N}.txt"
)

derivative_file = os.path.join(
    base_dir,
    "Data",
    "Eigen",
    "Derivatives",
    f"second_derivative_energy_data_{J1}_{J2}_{hx}_{hy}_{N}.txt"
)

if not os.path.exists(energy_file):
    print(f"Missing file: {energy_file}")
    sys.exit(1)

if not os.path.exists(derivative_file):
    print(f"Missing file: {derivative_file}")
    sys.exit(1)

# ============================================================
# Load data
# ============================================================

energy_data = np.loadtxt(energy_file)
derivative_data = np.loadtxt(derivative_file)

hz = energy_data[:, 2]
ground_energy = energy_data[:, 5]
second_derivative = derivative_data[:, 5]

# ============================================================
# Plot 1: Ground-state energy
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    hz,
    ground_energy,
    marker='o',
    linewidth=2
)

plt.xlabel(r"$h_z$")
plt.ylabel(r"Ground State Energy $E_0$")
plt.title(rf"N={N}, J1={J1/100.0}, J2={J2/100.0}, h_x={hx/100.0}, h_y={hy/100.0}")
plt.grid(True)
plt.tight_layout()

plot_dir = os.path.join(base_dir, "Plots")
os.makedirs(plot_dir, exist_ok=True)

plt.savefig(
    os.path.join(plot_dir, f"GroundStateEnergy_{N}_{J1}_{J2}_{hx}_{hy}.png"),
    dpi=300
)

#plt.show()

# ============================================================
# Plot 2: Second derivative
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    hz,
    second_derivative,
    marker='s',
    linewidth=2
)

plt.xlabel(r"$h_z$")
plt.ylabel(r"$d^2E/dh_z^2$")
plt.title(rf"Second Derivative, N={N}, J1={J1/100.0}, J2={J2/100.0}, h_x={hx/100.0}, h_y={hy/100.0}")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(plot_dir, f"SecondDerivative_{N}_{J1}_{J2}_{hx}_{hy}.png"),
    dpi=300
)

#plt.show()