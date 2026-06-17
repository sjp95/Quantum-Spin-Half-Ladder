#!/usr/bin/env python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Usage
#
# python3 PlotObservables.py \
# N SWEEP FIX_PARAMETER FIX_VALUES \
# J1 J2 HX HY HZ
#
# Example
#
# python3 PlotObservables.py \
# 12 J2 hz "0.0,0.5,1.0" \
# 1.0 0.0 0.0 0.0 0.0
#
# ==========================================================

if len(sys.argv) != 10:

    print(
        "Usage:\n"
        "python3 PlotObservables.py "
        "N SWEEP FIX_PARAMETER FIX_VALUES "
        "J1 J2 HX HY HZ"
    )

    sys.exit(1)

# ==========================================================
# Input
# ==========================================================

N = int(sys.argv[1])

SWEEP = sys.argv[2]

FIX_PARAMETER = sys.argv[3]

FIX_VALUES = [
    float(x)
    for x in sys.argv[4].split(",")
]

J1 = float(sys.argv[5])
J2 = float(sys.argv[6])

hx = float(sys.argv[7])
hy = float(sys.argv[8])
hz = float(sys.argv[9])

# ==========================================================
# Style
# ==========================================================

plt.rcParams["font.size"] = 20

try:
    plt.rcParams["font.family"] = "Times New Roman"
except:
    pass

# ==========================================================
# Helpers
# ==========================================================

def to100(x):
    return int(round(100*x))

BASE = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "Data"
    )
)

# ==========================================================
# GAP
# ==========================================================

def build_gap_file(fixed):

    J1i = to100(J1)
    J2i = to100(J2)

    hxi = to100(hx)
    hyi = to100(hy)
    hzi = to100(hz)

    if FIX_PARAMETER == "hz":
        hzi = to100(fixed)

    elif FIX_PARAMETER == "J2":
        J2i = to100(fixed)

    elif FIX_PARAMETER == "hx":
        hxi = to100(fixed)

    elif FIX_PARAMETER == "hy":
        hyi = to100(fixed)

    if SWEEP == "J2":

        return os.path.join(
            BASE,
            "Eigen",
            "Gap",
            f"Gap_vs_J2_N{N}_J1{J1i}_hx{hxi}_hy{hyi}_hz{hzi}.txt"
        )

    elif SWEEP == "hz":

        return os.path.join(
            BASE,
            "Eigen",
            "Gap",
            f"Gap_vs_hz_N{N}_J1{J1i}_J2{J2i}_hx{hxi}_hy{hyi}.txt"
        )

    elif SWEEP == "hx":

        return os.path.join(
            BASE,
            "Eigen",
            "Gap",
            f"Gap_vs_hx_N{N}_J1{J1i}_J2{J2i}_hy{hyi}_hz{hzi}.txt"
        )

    elif SWEEP == "hy":

        return os.path.join(
            BASE,
            "Eigen",
            "Gap",
            f"Gap_vs_hy_N{N}_J1{J1i}_J2{J2i}_hx{hxi}_hz{hzi}.txt"
        )
    
# ==========================================================
# D2E
# ==========================================================

def build_d2_file(fixed):

    J1i = to100(J1)
    J2i = to100(J2)

    hxi = to100(hx)
    hyi = to100(hy)
    hzi = to100(hz)

    if FIX_PARAMETER == "hz":
        hzi = to100(fixed)

    elif FIX_PARAMETER == "J2":
        J2i = to100(fixed)

    elif FIX_PARAMETER == "hx":
        hxi = to100(fixed)

    elif FIX_PARAMETER == "hy":
        hyi = to100(fixed)

    if SWEEP == "J2":

        return os.path.join(
            BASE,
            "Eigen",
            "Derivatives",
            f"D2E_vs_J2_N{N}_J1{J1i}_hx{hxi}_hy{hyi}_hz{hzi}.txt"
        )

    elif SWEEP == "hz":

        return os.path.join(
            BASE,
            "Eigen",
            "Derivatives",
            f"D2E_vs_hz_N{N}_J1{J1i}_J2{J2i}_hx{hxi}_hy{hyi}.txt"
        )

    elif SWEEP == "hx":

        return os.path.join(
            BASE,
            "Eigen",
            "Derivatives",
            f"D2E_vs_hx_N{N}_J1{J1i}_J2{J2i}_hy{hyi}_hz{hzi}.txt"
        )

    elif SWEEP == "hy":

        return os.path.join(
            BASE,
            "Eigen",
            "Derivatives",
            f"D2E_vs_hy_N{N}_J1{J1i}_J2{J2i}_hx{hxi}_hz{hzi}.txt"
        )
    
# ==========================================================
# NEMATIC
# ==========================================================

def build_nematic_file(fixed):

    J1i = to100(J1)
    J2i = to100(J2)

    hxi = to100(hx)
    hyi = to100(hy)
    hzi = to100(hz)

    if FIX_PARAMETER == "hz":
        hzi = to100(fixed)

    elif FIX_PARAMETER == "J2":
        J2i = to100(fixed)

    elif FIX_PARAMETER == "hx":
        hxi = to100(fixed)

    elif FIX_PARAMETER == "hy":
        hyi = to100(fixed)

    return os.path.join(
        BASE,
        "Nematic",
        "Combined",
        f"Nematic_vs_{SWEEP}_N{N}"
        f"_J1{J1i}"
        f"_hx{hxi}"
        f"_hy{hyi}"
        f"_hz{hzi}.txt"
    )

# ==========================================================
# CHIRALITY
# ==========================================================

def build_chiral_file(fixed):

    J1i = to100(J1)
    J2i = to100(J2)

    hxi = to100(hx)
    hyi = to100(hy)
    hzi = to100(hz)

    if FIX_PARAMETER == "hz":
        hzi = to100(fixed)

    elif FIX_PARAMETER == "J2":
        J2i = to100(fixed)

    elif FIX_PARAMETER == "hx":
        hxi = to100(fixed)

    elif FIX_PARAMETER == "hy":
        hyi = to100(fixed)

    return os.path.join(
        BASE,
        "Chirality",
        "Combined",
        f"Xavg_vs_{SWEEP}_N{N}"
        f"_J1{J1i}"
        f"_hx{hxi}"
        f"_hy{hyi}"
        f"_hz{hzi}.txt"
    )
# ==========================================================
# Figure
# ==========================================================

fig, ax = plt.subplots(
    1,
    4,
    figsize=(30,6)
)

titles = [
    "Gap",
    "Nematic",
    "Chirality",
    r"$d^2E/dx^2$"
]

for i in range(4):

    ax[i].set_title(titles[i])

    ax[i].set_box_aspect(1)

# ==========================================================
# Loop over fixed values
# ==========================================================

for fixed in FIX_VALUES:

    label = f"{FIX_PARAMETER}={fixed}"

    # ------------------------------------------------------
    # Gap
    # ------------------------------------------------------

    fgap = build_gap_file(fixed)

    print("Gap file =", fgap)

    if os.path.exists(fgap):

        try:

            data = np.loadtxt(fgap)

            if data.ndim == 1:
                data = data.reshape(1,-1)

            ax[0].plot(
                data[:,0],
                data[:,1],
                lw=3,
                label=label
            )

        except Exception as e:

            print("Cannot read:", fgap)
            print(e)

    else:

        print("Missing:", fgap)

    # ------------------------------------------------------
    # Nematic
    # ------------------------------------------------------

    fnem = build_nematic_file(fixed)

    print("Nematic file =", fnem)

    if os.path.exists(fnem):

        try:

            data = np.loadtxt(fnem)

            if data.ndim == 1:
                data = data.reshape(1,-1)

            ax[1].plot(
                data[:,0],
                data[:,1],
                lw=3,
                label=label
            )

        except Exception as e:

            print("Cannot read:", fnem)
            print(e)

    else:

        print("Missing:", fnem)

    # ------------------------------------------------------
    # Chirality
    # ------------------------------------------------------

    fchi = build_chiral_file(fixed)

    print("Chiral file =", fchi)

    if os.path.exists(fchi):

        try:

            data = np.loadtxt(fchi)

            if data.ndim == 1:
                data = data.reshape(1,-1)

            ax[2].plot(
                data[:,0],
                data[:,1],
                lw=3,
                label=label
            )

        except Exception as e:

            print("Cannot read:", fchi)
            print(e)

    else:

        print("Missing:", fchi)

    # ------------------------------------------------------
    # D2E
    # ------------------------------------------------------

    fd2 = build_d2_file(fixed)

    print("D2E file =", fd2)

    if os.path.exists(fd2):

        try:

            data = np.loadtxt(fd2)

            if data.ndim == 1:
                data = data.reshape(1,-1)

            ax[3].plot(
                data[:,0],
                data[:,1],
                lw=3,
                label=label
            )

        except Exception as e:

            print("Cannot read:", fd2)
            print(e)

    else:

        print("Missing:", fd2)

# ==========================================================
# Cosmetics
# ==========================================================

ylabel_list = [
    "Gap",
    "\langl D \rangl",
    r"$|X|$",
    r"$d^2E/dx^2$"
]

for i in range(4):

    ax[i].set_xlabel(SWEEP)

    ax[i].set_ylabel(
        ylabel_list[i]
    )

    handles, labels = ax[i].get_legend_handles_labels()

    if len(handles) > 0:

        ax[i].legend(
            frameon=False,
            fontsize=18
        )

    ax[i].tick_params(
        direction="in",
        length=8,
        width=2
    )

# ==========================================================
# Save figure
# ==========================================================

plot_dir = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "Plot"
    )
)

os.makedirs(
    plot_dir,
    exist_ok=True
)

outname = os.path.join(
    plot_dir,
    f"Observables_{SWEEP}_fixed_{FIX_PARAMETER}.pdf"
)

plt.savefig(
    outname,
    format="pdf",
    bbox_inches="tight"
)

print()
print("Saved figure:")
print(outname)
print()

plt.show()

print("\nSearching files:\n")

print(build_gap_file(FIX_VALUES[0]))
print(build_nematic_file(FIX_VALUES[0]))
print(build_chiral_file(FIX_VALUES[0]))
print(build_d2_file(FIX_VALUES[0]))
print()