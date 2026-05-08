import os
import glob
import sys


if len(sys.argv) < 4:
    print("Usage: Eh.py N Jx Jz")
    sys.exit(1)

N = int(sys.argv[1])
Jx = int(float(sys.argv[2]) * 100)
Jz = int(float(sys.argv[3]) * 100)

base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
data_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Magnetization"))
pattern = f"M_{N}_{Jx}_{Jz}_*.dat"

file_paths = glob.glob(os.path.join(data_dir, pattern))
if not file_paths:
    file_paths = glob.glob(os.path.join("..", "Data", "Magnetization", pattern))

if not file_paths:
    print(f"No files found for pattern: {os.path.join(data_dir, pattern)}")
    sys.exit(1)

all_data_lines = []

for file_path in sorted(file_paths):
    try:
        with open(file_path, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                try:
                    float(parts[0])
                except (ValueError, IndexError):
                    continue
                all_data_lines.append(line)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

all_data_lines.sort(key=lambda x: float(x.split()[0]))

output_path = os.path.normpath(
    os.path.join(
        base_dir,
        "..",
        "Data",
        "Magnetization",
        "Combined",
        f"combined_magnetization_data_{N}_{Jx}_{Jz}.txt",
    )
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as outfile:
    for line in all_data_lines:
        outfile.write(line + "\n")

print(f"Data successfully combined into combined_magnetization_data_{N}_{Jx}_{Jz}.txt")