#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# USER INPUT
# ==========================================================

N = 16

SWEEP = "J2"

FIX_PARAMETER = "hz"

FIX_VALUES = [0.0,0.5,1.0]

J1 = 1.0
J2 = 1.0

hx = 0.0
hy = 0.0
hz = 0.0

# ==========================================================
# Plot Style
# ==========================================================

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 30

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
# File Builders
# ==========================================================

def build_gap_file(fixed):

    J1i = to100(J1)
    J2i = to100(J2)

    hxi = to100(hx)
    hyi = to100(hy)
    hzi = to100(hz)

    if FIX_PARAMETER == "hz":

        hzi = to100(fixed)

        return os.path.join(
            BASE,
            "Eigen",
            "Gap",
            f"Gap_vs_{SWEEP}_N{N}_J1{J1i}_hx{hxi}_hy{hyi}_hz{hzi}.txt"
        )

    elif FIX_PARAMETER == "J2":

        J2i = to100(fixed)

        return os.path.join(
            BASE,
            "Eigen",
            "Gap",
            f"Gap_vs_{SWEEP}_N{N}_J1{J1i}_hx{hxi}_hy{hyi}_hz{hzi}.txt"
        )

    elif FIX_PARAMETER == "hx":

        hxi = to100(fixed)

        return os.path.join(
            BASE,
            "Eigen",
            "Gap",
            f"Gap_vs_{SWEEP}_N{N}_J1{J1i}_J2{J2i}_hy{hyi}_hz{hzi}.txt"
        )

    elif FIX_PARAMETER == "hy":

        hyi = to100(fixed)

        return os.path.join(
            BASE,
            "Eigen",
            "Gap",
            f"Gap_vs_{SWEEP}_N{N}_J1{J1i}_J2{J2i}_hx{hxi}_hz{hzi}.txt"
        )

# ==========================================================

def build_d2_file(fixed):

    return build_gap_file(fixed)\
        .replace("/Gap/","/Derivatives/")\
        .replace("Gap_","D2E_")

# ==========================================================

def build_nematic_file(fixed):

    return build_gap_file(fixed)\
        .replace("Eigen/Gap","Nematic/Combined")\
        .replace("Gap_","Nematic_")

# ==========================================================

def build_chiral_file(fixed):

    return build_gap_file(fixed)\
        .replace("Eigen/Gap","Chirality/Combined")\
        .replace("Gap_","Xavg_")

# ==========================================================
# Figure
# ==========================================================

fig, ax = plt.subplots(
    1,
    4,
    figsize=(24,6)
)

titles = [
    "Gap",
    "Nematic",
    "Chirality",
    r"$d^2E/dx^2$"
]

for i in range(4):

    ax[i].set_title(
        titles[i],
        fontsize=30
    )

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

    if os.path.exists(fgap):

        data = np.loadtxt(fgap)

        ax[0].plot(
            data[:,0],
            data[:,1],
            lw=3,
            label=label
        )

    # ------------------------------------------------------
    # Nematic
    # ------------------------------------------------------

    fnem = build_nematic_file(fixed)

    if os.path.exists(fnem):

        data = np.loadtxt(fnem)

        ax[1].plot(
            data[:,0],
            data[:,1],
            lw=3,
            label=label
        )

    # ------------------------------------------------------
    # Chirality
    # ------------------------------------------------------

    fchi = build_chiral_file(fixed)

    if os.path.exists(fchi):

        data = np.loadtxt(fchi)

        ax[2].plot(
            data[:,0],
            data[:,1],
            lw=3,
            label=label
        )

    # ------------------------------------------------------
    # D2E
    # ------------------------------------------------------

    fd2 = build_d2_file(fixed)

    if os.path.exists(fd2):

        data = np.loadtxt(fd2)

        ax[3].plot(
            data[:,0],
            data[:,1],
            lw=3,
            label=label
        )

# ==========================================================
# Cosmetics
# ==========================================================

for a in ax:

    a.set_xlabel(SWEEP)

    a.legend(
        fontsize=18,
        frameon=False
    )

    a.tick_params(
        width=2,
        length=8
    )

plt.tight_layout()

plt.show()