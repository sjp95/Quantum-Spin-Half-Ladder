import os
import glob
import sys
import h5py

# ============================================================
# Usage
#
# python3 Gap_hdf5.py N sweep J1 J2 hx hy hz
#
# Examples
#
# Sweep J2:
# python3 Gap_hdf5.py 12 J2 1.0 0.0 0.0 0.0 0.0
#
# Sweep hz:
# python3 Gap_hdf5.py 12 hz 1.0 1.0 0.0 0.0 0.0
#
# Sweep hx:
# python3 Gap_hdf5.py 12 hx 1.0 1.0 0.0 0.0 0.0
#
# Sweep hy:
# python3 Gap_hdf5.py 12 hy 1.0 1.0 0.0 0.0 0.0
# ============================================================

if len(sys.argv) < 8:
    print(
    "Usage:\n"
    "python3 Gap_hdf5.py N sweep J1 J2 hx hy hz"
    )
    sys.exit(1)

N      = int(sys.argv[1])
sweep  = sys.argv[2]

J1 = int(round(float(sys.argv[3])*100))
J2 = int(round(float(sys.argv[4])*100))
hx = int(round(float(sys.argv[5])*100))
hy = int(round(float(sys.argv[6])*100))
hz = int(round(float(sys.argv[7])*100))

# ============================================================
# Data directory
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.normpath(
    os.path.join(base_dir,
                 "..",
                 "Data",
                 "Eigen",
                 "Eigen")
)

# ============================================================
# Build search pattern
# ============================================================

if sweep == "J2":

    pattern = (
        f"EigenSpectrum_{N}_{J1}_*_{hx}_{hy}_{hz}.h5"
    )

elif sweep == "hz":

    pattern = (
        f"EigenSpectrum_{N}_{J1}_{J2}_{hx}_{hy}_*.h5"
    )

elif sweep == "hx":

    pattern = (
        f"EigenSpectrum_{N}_{J1}_{J2}_*_{hy}_{hz}.h5"
    )

elif sweep == "hy":

    pattern = (
        f"EigenSpectrum_{N}_{J1}_{J2}_{hx}_*_{hz}.h5"
    )

else:
    print("Unknown sweep variable")
    sys.exit(1)

file_paths = glob.glob(
    os.path.join(data_dir, pattern)
)

if not file_paths:
    print("No files found")
    print(pattern)
    sys.exit(1)

# ============================================================
# Extract sweep value
# ============================================================

def extract_variable(filepath):

    name = os.path.basename(filepath)

    parts = name.replace(".h5","").split("_")

    #
    # EigenSpectrum
    # N
    # J1
    # J2
    # hx
    # hy
    # hz
    #

    if sweep == "J2":
        return int(parts[3])

    elif sweep == "hx":
        return int(parts[4])

    elif sweep == "hy":
        return int(parts[5])

    elif sweep == "hz":
        return int(parts[6])

file_paths.sort(key=extract_variable)

# ============================================================
# Output
# ============================================================

output_dir = os.path.join(
    base_dir,
    "..",
    "Data",
    "Eigen",
    "Gap"
)

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    f"Gap_{sweep}_{N}.dat"
)

# ============================================================
# Compute gap
# ============================================================

with open(output_file, "w") as outfile:

    outfile.write(
        "# sweep E0 E1 Gap\n"
    )

    for filepath in file_paths:

        try:

            sweep_value = (
                extract_variable(filepath)/100.0
            )

            with h5py.File(filepath,"r") as f:

                eigs = f["eigenvalues"][:]

                eigs = eigs.flatten()

                eigs.sort()

                E0 = float(eigs[0])
                E1 = float(eigs[1])

                gap = E1 - E0

                outfile.write(
                    f"{sweep_value:.8f} "
                    f"{E0:.16e} "
                    f"{E1:.16e} "
                    f"{gap:.16e}\n"
                )

            print(
                f"Processed "
                f"{os.path.basename(filepath)}"
            )

        except Exception as e:

            print(
                f"Error reading "
                f"{filepath}: {e}"
            )

print("\nOutput written to:")
print(output_file)