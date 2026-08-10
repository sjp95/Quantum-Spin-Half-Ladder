#!/usr/bin/env python3

import os
import glob
import sys

# ============================================================
# Usage
#
# python3 combine_chirality.py N sweep J1 J2 hx hy hz
#
# Examples
#
# sweep J2:
# python3 combine_chirality.py 16 J2 1.0 0.0 0.0 0.0 0.0
#
# sweep hz:
# python3 combine_chirality.py 16 hz 1.0 1.0 0.0 0.0 0.0
#
# sweep hx:
# python3 combine_chirality.py 16 hx 1.0 1.0 0.0 0.0 0.0
#
# sweep hy:
# python3 combine_chirality.py 16 hy 1.0 1.0 0.0 0.0 0.0
#
# ============================================================

if len(sys.argv) != 8:
    print(
        "Usage:\n"
        "python3 combine_chirality.py "
        "N sweep J1 J2 hx hy hz"
    )
    sys.exit(1)

# ============================================================

N = int(sys.argv[1])

sweep = sys.argv[2]

J1 = int(round(float(sys.argv[3])*100))
J2 = int(round(float(sys.argv[4])*100))
hx = int(round(float(sys.argv[5])*100))
hy = int(round(float(sys.argv[6])*100))
hz = int(round(float(sys.argv[7])*100))

# ============================================================

allowed = ["J2","hx","hy","hz"]

if sweep not in allowed:
    print("Sweep must be one of:")
    print(allowed)
    sys.exit(1)

# ============================================================
# Paths
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.normpath(
    os.path.join(
        base_dir,
        "..",
        "Data",
        "Chirality"
    )
)

combined_dir = os.path.join(
    data_dir,
    "Combined"
)

os.makedirs(combined_dir, exist_ok=True)

# ============================================================
# File pattern
# ============================================================

if sweep == "J2":

    pattern = (
        f"Chirality_{N}_{J1}_*_{hx}_{hy}_{hz}.dat"
    )

elif sweep == "hx":

    pattern = (
        f"Chirality_{N}_{J1}_{J2}_*_{hy}_{hz}.dat"
    )

elif sweep == "hy":

    pattern = (
        f"Chirality_{N}_{J1}_{J2}_{hx}_*_{hz}.dat"
    )

elif sweep == "hz":

    pattern = (
        f"Chirality_{N}_{J1}_{J2}_{hx}_{hy}_*.dat"
    )

# ============================================================

file_paths = glob.glob(
    os.path.join(data_dir, pattern)
)

if not file_paths:
    print("No files found")
    print(pattern)
    sys.exit(1)

# ============================================================
# Extract sweep parameter
# ============================================================

def extract_value(filepath):

    name = os.path.basename(filepath)

    parts = name.replace(".dat","").split("_")

    #
    # Chirality_N_J1_J2_hx_hy_hz.dat
    #
    # index:
    #
    # 0 1 2 3 4 5 6
    #

    if sweep == "J2":
        return int(parts[3])

    elif sweep == "hx":
        return int(parts[4])

    elif sweep == "hy":
        return int(parts[5])

    elif sweep == "hz":
        return int(parts[6])

# ============================================================

file_paths.sort(key=extract_value)

# ============================================================
# Output names
# ============================================================

if sweep == "J2":

    suffix = (
        f"N{N}"
        f"_J1{J1}"
        f"_hx{hx}"
        f"_hy{hy}"
        f"_hz{hz}"
    )

elif sweep == "hx":

    suffix = (
        f"N{N}"
        f"_J1{J1}"
        f"_J2{J2}"
        f"_hy{hy}"
        f"_hz{hz}"
    )

elif sweep == "hy":

    suffix = (
        f"N{N}"
        f"_J1{J1}"
        f"_J2{J2}"
        f"_hx{hx}"
        f"_hz{hz}"
    )

elif sweep == "hz":

    suffix = (
        f"N{N}"
        f"_J1{J1}"
        f"_J2{J2}"
        f"_hx{hx}"
        f"_hy{hy}"
    )

# ============================================================

out_xx = os.path.join(
    combined_dir,
    f"Xx_vs_{sweep}_{suffix}.txt"
)

out_xz = os.path.join(
    combined_dir,
    f"Xz_vs_{sweep}_{suffix}.txt"
)

out_avg = os.path.join(
    combined_dir,
    f"Xavg_vs_{sweep}_{suffix}.txt"
)

# ============================================================
# Read files
# ============================================================

Xx_data = []
Xz_data = []
Xavg_data = []

for filepath in file_paths:

    try:

        with open(filepath,"r") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                vals = line.split()

                if len(vals) < 8:
                    continue

                hxv = float(vals[0])
                hyv = float(vals[1])
                hzv = float(vals[2])
                J1v = float(vals[3])
                J2v = float(vals[4])

                Xx = float(vals[5])
                Xz = float(vals[6])
                Xavg = float(vals[7])

                if sweep == "J2":
                    x = J2v

                elif sweep == "hx":
                    x = hxv

                elif sweep == "hy":
                    x = hyv

                elif sweep == "hz":
                    x = hzv

                Xx_data.append((x,Xx))
                Xz_data.append((x,Xz))
                Xavg_data.append((x,Xavg))

        print(
            "Processed:",
            os.path.basename(filepath)
        )

    except Exception as e:

        print(
            "Error:",
            filepath,
            e
        )

# ============================================================
# Sort
# ============================================================

Xx_data.sort(key=lambda t: t[0])
Xz_data.sort(key=lambda t: t[0])
Xavg_data.sort(key=lambda t: t[0])

# ============================================================
# Write
# ============================================================

with open(out_xx,"w") as f:

    for x,y in Xx_data:
        f.write(f"{x:.15e} {y:.15e}\n")

with open(out_xz,"w") as f:

    for x,y in Xz_data:
        f.write(f"{x:.15e} {y:.15e}\n")

with open(out_avg,"w") as f:

    for x,y in Xavg_data:
        f.write(f"{x:.15e} {y:.15e}\n")

# ============================================================

print()
print("Written:")
print(out_xx)
print(out_xz)
print(out_avg)
print()