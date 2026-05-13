import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Usage:
# python3 plot_energy.py N [J1] [J2]
#
# Example:
# python3 plot_energy.py 4 1.0 1.0
# ============================================================

if len(sys.argv) < 2:
    print("Usage: python3 plot_energy.py N [J1] [J2]")
    sys.exit(1)

N = int(sys.argv[1])

J1 = int(float(sys.argv[2]) * 100) if len(sys.argv) > 2 else 100
J2 = int(float(sys.argv[3]) * 100) if len(sys.argv) > 3 else 100

# ============================================================
# File path
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.normpath(
    os.path.join(
        base_dir,
        "Data",
        "Eigen",
        "Combined",
        f"combined_energy_data_{J1}_{J2}_{N}.txt"
    )
)

if not os.path.exists(input_file):
    print(f"File not found: {input_file}")
    sys.exit(1)

# ============================================================
# Read data
# ============================================================

data = np.loadtxt(input_file)

hz = data[:, 0]
ground_energy = data[:, 3]

# ============================================================
# Plot
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    hz,
    ground_energy,
    marker='o',
    linestyle='-',
    linewidth=2
)

plt.xlabel(r"$h_z$", fontsize=14)
plt.ylabel(r"Ground State Energy $E_0$", fontsize=14)

plt.title(
    rf"N={N}, J1={J1/100.0}, J2={J2/100.0}",
    fontsize=14
)

plt.grid(True)
plt.tight_layout()

# ============================================================
# Save plot
# ============================================================

output_dir = os.path.normpath(
    os.path.join(base_dir,"Plots")
)

os.makedirs(output_dir, exist_ok=True)

plot_file = os.path.join(
    output_dir,
    f"GroundStateEnergy_{N}_{J1}_{J2}.png"
)

plt.savefig(plot_file, dpi=300)

print(f"Plot saved to: {plot_file}")

plt.show()