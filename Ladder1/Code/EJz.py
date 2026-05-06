import os
import glob
import sys

# Parameters
if len(sys.argv) < 2:
    print("Usage: EJz.py N [hz] [Jx]")
    sys.exit(1)

N = int(sys.argv[1])
hz = int(float(sys.argv[2]) * 100) if len(sys.argv) > 2 else 0
Jx = int(float(sys.argv[3]) * 100) if len(sys.argv) > 3 else 100

# Read all matching files
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Energy"))
pattern = f"E_{N}_{Jx}_*_{hz}.dat"
file_paths = glob.glob(os.path.join(data_dir, pattern))
if not file_paths:
    file_paths = glob.glob(os.path.join(base_dir, "..", "Data", "Energy", pattern))
if not file_paths:
    print(f"No files found for pattern: {os.path.join(data_dir, pattern)}")

# Sort files to process in order
file_paths.sort()

# Read all data lines and sort by Kitayev.h
all_data_lines = []

for file_path in file_paths:
    try:
        with open(file_path, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                first_tok = line.split()[0]
                try:
                    float(first_tok)
                except ValueError:
                    continue
                all_data_lines.append(line)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Sort by the first column (Kitayev.h)
all_data_lines.sort(key=lambda x: float(x.split()[0]))

# Write results to a single output file
output_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Energy", "Combined"))
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"combined_energy_data_{Jx}_{hz}_{N}.txt")

with open(output_path, "w") as outfile:
    for line in all_data_lines:
        outfile.write(line + "\n")

print(f"Data successfully combined into combined_energy_data_{Jx}_{hz}_{N}.txt")
