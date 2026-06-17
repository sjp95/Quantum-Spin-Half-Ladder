```python
import os
import glob
import sys
import h5py
import numpy as np

# ============================================================
# Usage
#
# python3 EnergyAnalysis.py N mode sweep J1 J2 hx hy hz
#
# mode:
#   energy
#   gap
#   d2
#
# sweep:
#   J1
#   J2
#   hx
#   hy
#   hz
#
# Example:
#
# python3 EnergyAnalysis.py 16 energy hz 1.0 1.0 0.0 0.0 0.0
#
# python3 EnergyAnalysis.py 16 gap J2 1.0 0.0 0.0 0.0 0.0
#
# python3 EnergyAnalysis.py 16 d2 J2 1.0 0.0 0.0 0.0 0.0
#
# ============================================================

if len(sys.argv) != 9:
    print(
        "Usage:\n"
        "python3 EnergyAnalysis.py "
        "N mode sweep J1 J2 hx hy hz"
    )
    sys.exit(1)

# ============================================================
# Input
# ============================================================

N = int(sys.argv[1])

mode  = sys.argv[2]
sweep = sys.argv[3]

J1 = int(round(float(sys.argv[4])*100))
J2 = int(round(float(sys.argv[5])*100))
hx = int(round(float(sys.argv[6])*100))
hy = int(round(float(sys.argv[7])*100))
hz = int(round(float(sys.argv[8])*100))

# ============================================================
# Directories
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.normpath(
    os.path.join(
        base_dir,
        "..",
        "Data",
        "Eigen",
        "Eigen"
    )
)

# ============================================================
# File pattern
# EigenSpectrum_N_J1_J2_hx_hy_hz.h5
# ============================================================

if sweep == "J1":

    pattern = (
        f"EigenSpectrum_{N}_*_{J2}_{hx}_{hy}_{hz}.h5"
    )

    def extract_parameter(filepath):
        return int(
            os.path.basename(filepath)
            .replace(".h5","")
            .split("_")[2]
        )

elif sweep == "J2":

    pattern = (
        f"EigenSpectrum_{N}_{J1}_*_{hx}_{hy}_{hz}.h5"
    )

    def extract_parameter(filepath):
        return int(
            os.path.basename(filepath)
            .replace(".h5","")
            .split("_")[3]
        )

elif sweep == "hx":

    pattern = (
        f"EigenSpectrum_{N}_{J1}_{J2}_*_{hy}_{hz}.h5"
    )

    def extract_parameter(filepath):
        return int(
            os.path.basename(filepath)
            .replace(".h5","")
            .split("_")[4]
        )

elif sweep == "hy":

    pattern = (
        f"EigenSpectrum_{N}_{J1}_{J2}_{hx}_*_{hz}.h5"
    )

    def extract_parameter(filepath):
        return int(
            os.path.basename(filepath)
            .replace(".h5","")
            .split("_")[5]
        )

elif sweep == "hz":

    pattern = (
        f"EigenSpectrum_{N}_{J1}_{J2}_{hx}_{hy}_*.h5"
    )

    def extract_parameter(filepath):
        return int(
            os.path.basename(filepath)
            .replace(".h5","")
            .split("_")[6]
        )

else:

    print("Unknown sweep parameter")
    sys.exit(1)

# ============================================================
# Locate files
# ============================================================

file_paths = glob.glob(
    os.path.join(data_dir, pattern)
)

if len(file_paths) == 0:

    print(
        f"No files found for pattern:\n{pattern}"
    )
    sys.exit(1)

file_paths.sort(key=extract_parameter)

# ============================================================
# Output directories
# ============================================================

energy_dir = os.path.join(
    base_dir,
    "..",
    "Data",
    "Eigen",
    "Energy"
)

gap_dir = os.path.join(
    base_dir,
    "..",
    "Data",
    "Eigen",
    "Gap"
)

derivative_dir = os.path.join(
    base_dir,
    "..",
    "Data",
    "Eigen",
    "Derivatives"
)

os.makedirs(energy_dir, exist_ok=True)
os.makedirs(gap_dir, exist_ok=True)
os.makedirs(derivative_dir, exist_ok=True)

# ============================================================
# Output names
# ============================================================

if sweep == "J1":

    energy_output = os.path.join(
        energy_dir,
        f"Energy_vs_J1_N{N}_J2{J2}_hx{hx}_hy{hy}_hz{hz}.txt"
    )

    gap_output = os.path.join(
        gap_dir,
        f"Gap_vs_J1_N{N}_J2{J2}_hx{hx}_hy{hy}_hz{hz}.txt"
    )

    derivative_output = os.path.join(
        derivative_dir,
        f"D2E_vs_J1_N{N}_J2{J2}_hx{hx}_hy{hy}_hz{hz}.txt"
    )

elif sweep == "J2":

    energy_output = os.path.join(
        energy_dir,
        f"Energy_vs_J2_N{N}_J1{J1}_hx{hx}_hy{hy}_hz{hz}.txt"
    )

    gap_output = os.path.join(
        gap_dir,
        f"Gap_vs_J2_N{N}_J1{J1}_hx{hx}_hy{hy}_hz{hz}.txt"
    )

    derivative_output = os.path.join(
        derivative_dir,
        f"D2E_vs_J2_N{N}_J1{J1}_hx{hx}_hy{hy}_hz{hz}.txt"
    )

elif sweep == "hx":

    energy_output = os.path.join(
        energy_dir,
        f"Energy_vs_hx_N{N}_J1{J1}_J2{J2}_hy{hy}_hz{hz}.txt"
    )

    gap_output = os.path.join(
        gap_dir,
        f"Gap_vs_hx_N{N}_J1{J1}_J2{J2}_hy{hy}_hz{hz}.txt"
    )

    derivative_output = os.path.join(
        derivative_dir,
        f"D2E_vs_hx_N{N}_J1{J1}_J2{J2}_hy{hy}_hz{hz}.txt"
    )

elif sweep == "hy":

    energy_output = os.path.join(
        energy_dir,
        f"Energy_vs_hy_N{N}_J1{J1}_J2{J2}_hx{hx}_hz{hz}.txt"
    )

    gap_output = os.path.join(
        gap_dir,
        f"Gap_vs_hy_N{N}_J1{J1}_J2{J2}_hx{hx}_hz{hz}.txt"
    )

    derivative_output = os.path.join(
        derivative_dir,
        f"D2E_vs_hy_N{N}_J1{J1}_J2{J2}_hx{hx}_hz{hz}.txt"
    )

elif sweep == "hz":

    energy_output = os.path.join(
        energy_dir,
        f"Energy_vs_hz_N{N}_J1{J1}_J2{J2}_hx{hx}_hy{hy}.txt"
    )

    gap_output = os.path.join(
        gap_dir,
        f"Gap_vs_hz_N{N}_J1{J1}_J2{J2}_hx{hx}_hy{hy}.txt"
    )

    derivative_output = os.path.join(
        derivative_dir,
        f"D2E_vs_hz_N{N}_J1{J1}_J2{J2}_hx{hx}_hy{hy}.txt"
    )

# ============================================================
# Read spectra
# ============================================================

xvals = []
E0vals = []
Gapvals = []

for filepath in file_paths:

    try:

        x = extract_parameter(filepath)/100.0

        with h5py.File(filepath,"r") as f:

            eigs = np.array(
                f["eigenvalues"][:]
            ).flatten()

        eigs = np.sort(eigs)

        E0 = float(eigs[0])

        tol = 1e-10

        gap = 0.0

        for e in eigs[1:]:

            if e - E0 > tol:
                gap = float(e - E0)
                break

        xvals.append(x)
        E0vals.append(E0)
        Gapvals.append(gap)

        print(
            f"Processed: "
            f"{os.path.basename(filepath)}"
        )

    except Exception as e:

        print(
            f"Error reading "
            f"{filepath}: {e}"
        )

xvals = np.array(xvals)
E0vals = np.array(E0vals)
Gapvals = np.array(Gapvals)

# ============================================================
# Energy
# ============================================================

if mode == "energy":

    with open(energy_output,"w") as f:

        for x,e0 in zip(xvals,E0vals):

            f.write(
                f"{x:.12e} {e0:.16e}\n"
            )

    print(
        f"\nEnergy data written to:\n"
        f"{energy_output}"
    )

# ============================================================
# Gap
# ============================================================

elif mode == "gap":

    with open(gap_output,"w") as f:

        for x,gap in zip(xvals,Gapvals):

            f.write(
                f"{x:.12e} {gap:.16e}\n"
            )

    print(
        f"\nGap data written to:\n"
        f"{gap_output}"
    )

# ============================================================
# Second derivative
# ============================================================

elif mode == "d2":

    def second_derivative_4th_order(x,y):

        n = len(x)

        if n < 5:
            return np.gradient(
                np.gradient(y,x),
                x
            )

        dx = np.diff(x)

        if not np.allclose(dx,dx[0]):
            return np.gradient(
                np.gradient(y,x),
                x
            )

        h = dx[0]

        d2 = np.zeros(n)

        for i in range(2,n-2):

            d2[i] = (
                -y[i+2]
                +16*y[i+1]
                -30*y[i]
                +16*y[i-1]
                -y[i-2]
            )/(12*h*h)

        d2[1] = (
            y[0]-2*y[1]+y[2]
        )/(h*h)

        d2[-2] = (
            y[-3]-2*y[-2]+y[-1]
        )/(h*h)

        d2[0] = (
            2*y[0]
            -5*y[1]
            +4*y[2]
            -y[3]
        )/(h*h)

        d2[-1] = (
            2*y[-1]
            -5*y[-2]
            +4*y[-3]
            -y[-4]
        )/(h*h)

        return d2

    d2E = second_derivative_4th_order(
        xvals,
        E0vals
    )

    with open(derivative_output,"w") as f:

        for x,val in zip(xvals,d2E):

            f.write(
                f"{x:.12e} {val:.16e}\n"
            )

    print(
        f"\nDerivative data written to:\n"
        f"{derivative_output}"
    )

else:

    print(
        "mode must be: "
        "energy, gap, or d2"
    )
```
