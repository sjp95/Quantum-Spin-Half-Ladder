import os
import glob
import sys
import h5py

# ============================================================
# Usage:
# python3 Eh_hdf5.py N [J1] [J2]
#
# Example:
# python3 Eh_hdf5.py 4 1.0 1.0
# ============================================================

if len(sys.argv) < 2:
    print("Usage: python3 Eh_hdf5.py N [J1] [J2]")
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
    os.path.join(base_dir, "..", "Data", "Eigen", "Eigen")
)

pattern = f"EigenSpectrum_{N}_{J1}_{J2}_{hx}_{hy}_*.h5"

file_paths = glob.glob(os.path.join(data_dir, pattern))

if not file_paths:
    print(f"No files found for pattern: {pattern}")
    sys.exit(1)

# ============================================================
# Extract hz from filename
# Filename format:
# EigenSpectrum_N_J1_J2_hz.h5
# ============================================================

def extract_hz(filepath):
    name = os.path.basename(filepath)
    parts = name.replace(".h5", "").split("_")
    return int(parts[-1])

file_paths.sort(key=extract_hz)

# ============================================================
# Output
# ============================================================

output_dir = os.path.join("..", "Data", "Eigen", "Combined")
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    f"combined_energy_data_{J1}_{J2}_{hx}_{hy}_{N}.txt"
)

# ============================================================
# Read HDF5 and extract only ground-state energy
# ============================================================

with open(output_file, "w") as outfile:

    for filepath in file_paths:
        try:
            hz = extract_hz(filepath)

            with h5py.File(filepath, "r") as f:
                eigenvalues = f["eigenvalues"][:]

                ground_energy = float(eigenvalues.flatten()[0])

                outfile.write(
                    f"{hz/100.0} {hx/100.0} {hy/100.0} {J1/100.0} {J2/100.0} {ground_energy}\n"
                )

            print(f"Processed: {os.path.basename(filepath)}")

        except Exception as e:
            print(f"Error reading {filepath}: {e}")
#============================================================#
#============================================================#



# import os
# import glob
# import sys
# import h5py
# import numpy as np

# # ============================================================
# # Argument parsing
# # Usage:
# # python3 combine_eigen.py N [J1] [J2]
# # Example:
# # python3 combine_eigen.py 4 1.0 1.0
# # ============================================================

# if len(sys.argv) < 2:
#     print("Usage: python3 combine_eigen.py N [J1] [J2]")
#     sys.exit(1)

# N = int(sys.argv[1])
# J1 = int(float(sys.argv[2]) * 100) if len(sys.argv) > 2 else 100
# J2 = int(float(sys.argv[3]) * 100) if len(sys.argv) > 3 else 100

# # ============================================================
# # Paths
# # ============================================================

# base_dir = os.path.dirname(os.path.abspath(__file__))

# data_dir = os.path.normpath(
#     os.path.join(base_dir, "..", "Data", "Eigen")
# )

# pattern = f"EigenSpectrum_{N}_{J1}_{J2}_*.h5"

# file_paths = glob.glob(os.path.join(data_dir, pattern))

# if not file_paths:
#     print(f"No files found for pattern: {os.path.join(data_dir, pattern)}")
#     sys.exit(1)

# # Sort by hz encoded in filename
# def extract_hz(filepath):
#     name = os.path.basename(filepath)
#     # EigenSpectrum_N_J1_J2_hz.h5
#     parts = name.replace(".h5", "").split("_")
#     return int(parts[-1])

# file_paths.sort(key=extract_hz)

# # ============================================================
# # Output
# # ============================================================

# output_dir = os.path.join(data_dir, "Combined")
# os.makedirs(output_dir, exist_ok=True)

# output_file = os.path.join(
#     output_dir,
#     f"CombinedEigenSpectrum_{N}_{J1}_{J2}.h5"
# )

# # ============================================================
# # Combine data
# # ============================================================

# all_eigenvalues = []
# all_eigenvectors = []
# all_hz = []

# for filepath in file_paths:
#     try:
#         hz = extract_hz(filepath)

#         with h5py.File(filepath, "r") as f:
#             eigenvalues = f["eigenvalues"][:]
#             eigenvectors = f["eigenvectors"][:]

#             all_eigenvalues.append(eigenvalues)
#             all_eigenvectors.append(eigenvectors)
#             all_hz.append(hz)

#             print(f"Loaded: {os.path.basename(filepath)}")

#     except Exception as e:
#         print(f"Error reading {filepath}: {e}")

# if not all_eigenvalues:
#     print("No valid HDF5 data found.")
#     sys.exit(1)

# # Convert to arrays
# all_eigenvalues = np.array(all_eigenvalues)
# all_eigenvectors = np.array(all_eigenvectors)
# all_hz = np.array(all_hz)

# # ============================================================
# # Write combined HDF5
# # ============================================================

# with h5py.File(output_file, "w") as f:
#     f.create_dataset("hz", data=all_hz)
#     f.create_dataset("eigenvalues", data=all_eigenvalues)
#     f.create_dataset("eigenvectors", data=all_eigenvectors)

# print(f"\nCombined HDF5 written to:\n{output_file}")