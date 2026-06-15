import os
import glob
import sys

# ============================================================
# Usage:
#
# python3 combine_nematic.py N J1 hx hy hz
#
# Example:
#
# python3 combine_nematic.py 16 1.0 0.0 0.0 0.0
#
# ============================================================

if len(sys.argv) < 6:
    print(
        "Usage: python3 combine_nematic.py "
        "N J1 hx hy hz"
    )
    sys.exit(1)

N  = int(sys.argv[1])

J1 = int(round(float(sys.argv[2])*100))
hx = int(round(float(sys.argv[3])*100))
hy = int(round(float(sys.argv[4])*100))
hz = int(round(float(sys.argv[5])*100))

# ============================================================
# Paths
# ============================================================

base_dir = os.path.dirname(
    os.path.abspath(__file__)
)

data_dir = os.path.normpath(
    os.path.join(
        base_dir,
        "..",
        "Data",
        "Nematic"
    )
)

# ============================================================
# Pattern
#
# D_N_J1_J2_hx_hy_hz.dat
#       ^
#       variable
# ============================================================

pattern = f"D_{N}_{J1}_*_{hx}_{hy}_{hz}.dat"

file_paths = glob.glob(
    os.path.join(data_dir, pattern)
)

if not file_paths:
    print(f"No files found for pattern:\n{pattern}")
    sys.exit(1)

# ============================================================
# Extract J2 from filename
# ============================================================

def extract_j2(filepath):

    name = os.path.basename(filepath)

    parts = name.replace(".dat","").split("_")

    # D_N_J1_J2_hx_hy_hz

    return int(parts[3])

# ============================================================
# Sort by J2
# ============================================================

file_paths.sort(key=extract_j2)

# ============================================================
# Output directory
# ============================================================

output_dir = os.path.join(
    data_dir,
    "..",
    "CombinedNematic"
)

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    f"combined_nematic_{N}_{J1}_{hx}_{hy}_{hz}.txt"
)

# ============================================================
# Read files
# ============================================================

all_data_lines = []

for filepath in file_paths:

    try:

        with open(filepath,"r") as infile:

            for line in infile:

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                parts = line.split()

                try:
                    float(parts[0])
                except ValueError:
                    continue

                all_data_lines.append(line)

        print(
            f"Processed: "
            f"{os.path.basename(filepath)}"
        )

    except Exception as e:

        print(
            f"Error reading "
            f"{filepath}: {e}"
        )

# ============================================================
# Sort by J2 value contained in data file
#
# file format:
#
# hx hy hz J1 J2 D
#
# J2 = column 5
# ============================================================

all_data_lines.sort(
    key=lambda x: float(x.split()[4])
)

# ============================================================
# Write combined file
# ============================================================

with open(output_file,"w") as outfile:

    outfile.write(
        "# hx hy hz J1 J2 D\n"
    )

    for line in all_data_lines:
        outfile.write(line + "\n")

print(
    "\nCombined nematic data written to:\n"
    + output_file
)