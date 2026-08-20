import os
import glob
import sys

# ============================================================
# Usage:
# python3 combine_sx.py N [J1] [J2]
#
# Example:
# python3 combine_sx.py 4 1.0 1.0
# ============================================================

if len(sys.argv) < 2:
    print("Usage: python3 combine_sx.py N [J1] [J2]")
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
    os.path.join(base_dir, "..", "Data", "Magnetization", "Sx")
)

pattern = f"Sz_{N}_{J1}_{J2}_{hx}_{hy}_*.dat"

file_paths = glob.glob(os.path.join(data_dir, pattern))

if not file_paths:
    print(f"No files found for pattern: {pattern}")
    sys.exit(1)

# ============================================================
# Sort by hz
# ============================================================

def extract_hz(filepath):
    name = os.path.basename(filepath)
    parts = name.replace(".dat", "").split("_")
    return int(parts[-1])

file_paths.sort(key=extract_hz)

# ============================================================
# Output
# ============================================================

output_dir = os.path.join(data_dir, "..", "CombinedSx")
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    f"combined_sz_data_{J1}_{J2}_{hx}_{hy}_{N}.txt"
)

# ============================================================
# Combine
# ============================================================

all_data_lines = []

for filepath in file_paths:
    try:
        with open(filepath, "r") as infile:
            for line in infile:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = line.split()

                try:
                    float(parts[0])
                except ValueError:
                    continue

                all_data_lines.append(line)

        print(f"Processed: {os.path.basename(filepath)}")

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

# sort by hz
all_data_lines.sort(key=lambda x: float(x.split()[0]))

# write
with open(output_file, "w") as outfile:
    for line in all_data_lines:
        outfile.write(line + "\n")

print(f"\nCombined Sx data written to:\n{output_file}")