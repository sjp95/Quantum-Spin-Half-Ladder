#!/usr/bin/env python3

import os
import glob
import sys

# ============================================================

# Usage

#

# python3 combine_nematic.py N sweep J1 J2 hx hy hz

#

# Examples

#

# python3 combine_nematic.py 16 J2 1.0 0.0 0.0 0.0 0.0

#

# python3 combine_nematic.py 16 hz 1.0 1.0 0.0 0.0 0.0

#

# python3 combine_nematic.py 16 hx 1.0 1.0 0.0 0.0 0.0

#

# python3 combine_nematic.py 16 hy 1.0 1.0 0.0 0.0 0.0

#

# ============================================================

if len(sys.argv) != 8:


print(
    "Usage:\n"
    "python3 combine_nematic.py "
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

base_dir = os.path.dirname(
os.path.abspath(**file**)
)

data_dir = os.path.normpath(
os.path.join(
base_dir,
"..",
"Data",
"Nematic"
)
)

combined_dir = os.path.join(
data_dir,
"Combined"
)

os.makedirs(
combined_dir,
exist_ok=True
)

# ============================================================

# File pattern

#

# D_N_J1_J2_hx_hy_hz.dat

# ============================================================

if sweep == "J2":


pattern = (
    f"D_{N}_{J1}_*_{hx}_{hy}_{hz}.dat"
)


elif sweep == "hx":


pattern = (
    f"D_{N}_{J1}_{J2}_*_{hy}_{hz}.dat"
)


elif sweep == "hy":


pattern = (
    f"D_{N}_{J1}_{J2}_{hx}_*_{hz}.dat"
)


elif sweep == "hz":


pattern = (
    f"D_{N}_{J1}_{J2}_{hx}_{hy}_*.dat"
)


# ============================================================

file_paths = glob.glob(
os.path.join(
data_dir,
pattern
)
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

parts = name.replace(
    ".dat",
    ""
).split("_")

#
# D_N_J1_J2_hx_hy_hz
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

file_paths.sort(
key=extract_value
)

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

output_file = os.path.join(
combined_dir,
f"Nematic_vs_{sweep}_{suffix}.txt"
)

# ============================================================

# Read files

# ============================================================

nematic_data = []

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

            if len(vals) < 6:
                continue

            hxv = float(vals[0])
            hyv = float(vals[1])
            hzv = float(vals[2])
            J1v = float(vals[3])
            J2v = float(vals[4])

            D = float(vals[5])

            if sweep == "J2":
                x = J2v

            elif sweep == "hx":
                x = hxv

            elif sweep == "hy":
                x = hyv

            elif sweep == "hz":
                x = hzv

            nematic_data.append(
                (x,D)
            )

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

nematic_data.sort(
key=lambda t: t[0]
)

# ============================================================

# Write

# ============================================================

with open(output_file,"w") as f:


for x,y in nematic_data:

    f.write(
        f"{x:.15e} {y:.15e}\n"
    )


# ============================================================

print()
print("Written:")
print(output_file)
print()
