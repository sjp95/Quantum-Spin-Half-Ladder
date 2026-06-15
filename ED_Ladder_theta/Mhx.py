import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Usage:
# python3 plot_sz.py N [J1] [J2]
#
# Example:
# python3 plot_sz.py 4 1.0 1.0
# ============================================================

if len(sys.argv) < 2:
    print("Usage: python3 plot_sz.py N [J1] [J2]")
    sys.exit(1)

N = int(sys.argv[1])

J1 = int(float(sys.argv[2]) * 100) if len(sys.argv) > 2 else 100
J2 = int(float(sys.argv[3]) * 100) if len(sys.argv) > 3 else 100
hy = int(float(sys.argv[4]) * 100) if len(sys.argv) > 4 else 100
hz = int(float(sys.argv[5]) * 100) if len(sys.argv) > 5 else 100

# ============================================================
# File path
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.normpath(
    os.path.join(
        base_dir,
        "Data",
        "Magnetization",
        "CombinedSx",
        f"combined_sx_data_{J1}_{J2}_{hy}_{hz}_{N}.txt"
    )
)

if not os.path.exists(input_file):
    print(f"File not found: {input_file}")
    sys.exit(1)

# ============================================================
# Read data
# ============================================================

data = np.loadtxt(input_file)

hx = data[:, 0]
sx = data[:, 5]

# ============================================================
# Plot
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    hx,
    sx,
    marker='o',
    linestyle='-',
    linewidth=2
)

plt.xlabel(r"$h_x$", fontsize=14)
plt.ylabel(r"$\langle S_x \rangle$", fontsize=14)

plt.title(
    rf"N={N}, J1={J1/100.0}, J2={J2/100.0}, h_y={hy/100.0}, h_z={hz/100.0}",
    fontsize=14
)

plt.grid(True)
plt.tight_layout()

# ============================================================
# Save
# ============================================================

output_dir = os.path.normpath(
    os.path.join(base_dir, "Plots")
)

os.makedirs(output_dir, exist_ok=True)

plot_file = os.path.join(
    output_dir,
    f"Sx_vs_hx_{N}_{J1}_{J2}_{hy}_{hz}.png"
)

plt.savefig(plot_file, dpi=300)

print(f"Plot saved to: {plot_file}")

plt.show()