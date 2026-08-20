import sys
import os
import math
import numpy as np
import h5py
import qkrylov

def main():
    if len(sys.argv) < 8:
        print("Usage: python3 st1.py N T J1 J2 hx hy hz [bc]")
        sys.exit(1)

    N = int(sys.argv[1])
    T = float(sys.argv[2])
    J1 = float(sys.argv[3]) / 100.0
    J2 = float(sys.argv[4]) / 100.0
    hx = float(sys.argv[5]) / 100.0
    hy = float(sys.argv[6]) / 100.0
    hz = float(sys.argv[7]) / 100.0

    if len(sys.argv) > 8:
        bc = sys.argv[8]
    else:
        bc = "obc"

    # Match system output style of st1.cpp / master.hpp
    print("===============================")
    print(f"hx: {hx}")
    print(f"hy: {hy}")
    print(f"hz: {hz}")
    print(f"Jx: {J1}")
    print(f"Jz: {J2}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    eigen_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Eigen", "Eigen"))
    os.makedirs(eigen_dir, exist_ok=True)

    # Construct output file name matching C++ exactly
    J1_rounded = int(round(J1 * 100.0))
    J2_rounded = int(round(J2 * 100.0))
    hx_rounded = int(round(hx * 100.0))
    hy_rounded = int(round(hy * 100.0))
    hz_rounded = int(round(hz * 100.0))

    outfile = os.path.join(
        eigen_dir,
        f"EigenSpectrum_{N}_{J1_rounded}_{J2_rounded}_{hx_rounded}_{hy_rounded}_{hz_rounded}.h5"
    )
    print(f"Output file: {outfile}")
    print("===============================")

    # Setup qkrylov spin basis & site
    basis = qkrylov.SpinHalfBasis(N)
    site = qkrylov.SpinHalfSite()

    # 1. Build coupling matrices Jx and Jz
    Jx_mat = np.zeros((N, N))
    Jz_mat = np.zeros((N, N))

    Nx = N // 2
    periodic = (bc.lower() == "pbc")

    for k in range(N):
        x = k // 2
        y = k % 2

        xp = (x + 1) % Nx
        yp = (y + 1) % 2

        kxp = xp * 2 + y
        kyp = x * 2 + yp

        if periodic or x < Nx - 1:
            Jx_mat[k, kxp] = J1
            Jx_mat[kxp, k] = J1

        Jz_mat[k, kyp] = J2
        Jz_mat[kyp, k] = J2

    # 2. Build qkrylov OpSum Hamiltonian using user's preferred tuple syntax
    ops = qkrylov.OpSum()

    # Add unique leg (Jx) and rung (Jz) couplings
    for i in range(N):
        for j in range(i + 1, N):
            if Jx_mat[i, j] != 0.0:
                ops += Jx_mat[i, j], 'Sx', i, 'Sx', j
            if Jz_mat[i, j] != 0.0:
                ops += Jz_mat[i, j], 'Sz', i, 'Sz', j

    # Add magnetic field terms
    for i in range(N):
        if hx != 0.0:
            ops += -hx, 'Sx', i
        if hy != 0.0:
            ops += -hy, 'Sy', i
        if hz != 0.0:
            ops += -hz, 'Sz', i

    H = qkrylov.MatrixFreeHamiltonian(basis, site, ops)
    print("===============================")
    print("H generated")

    # Solve for eigenvalues and eigenvectors
    # Lanczos ground state
    print("Solving for ground state using Lanczos...")
    eg = qkrylov.lanczos_ground_state(H)
    print(f"Ground state energy (Lanczos): {eg.energy:.16f}")

    # Davidson for lowest 2 eigenvalues to compute the gap
    print("Solving for lowest 2 eigenpairs using Davidson...")
    n_eig = min(2, H.dimension)
    ed = qkrylov.davidson_lowest(H, n_eig=n_eig)
    print(f"Davidson eigenvalues: {ed.eigenvalues}")

    # Write to HDF5 file
    with h5py.File(outfile, "w") as f:
        f.create_dataset("eigenvalues", data=ed.eigenvalues)
        evs_matrix = np.column_stack(ed.eigenvectors)
        f.create_dataset("eigenvectors", data=evs_matrix)

    print("HDF5 write successful")

    # The ground state eigenvector is the first column
    psi = ed.eigenvectors[0]
    le = H.dimension

    # 3. Compute Observables
    # Nematic Order Parameter D
    nematic_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Nematic"))
    os.makedirs(nematic_dir, exist_ok=True)
    nem_file = os.path.join(
        nematic_dir,
        f"D_{N}_{J1_rounded}_{J2_rounded}_{hx_rounded}_{hy_rounded}_{hz_rounded}.dat"
    )

    r = N // 2
    x_c = r // 2
    y_c = r % 2
    xp = (x_c + 1) % Nx
    yp = (y_c + 1) % 2
    rx = xp * 2 + y_c
    rz = x_c * 2 + yp

    n_indices = np.arange(le)
    sr = (n_indices >> r) & 1
    srx = (n_indices >> rx) & 1
    srz = (n_indices >> rz) & 1

    prob = np.abs(psi)**2

    # flip r and rx
    q = n_indices ^ (1 << r) ^ (1 << rx)
    sxsx = 0.25 * np.sum(np.real(np.conj(psi[q]) * psi))

    szsz = np.sum(prob * (sr - 0.5) * (srz - 0.5))

    Dval = 4.0 * (sxsx - szsz)

    with open(nem_file, "w") as f_nem:
        f_nem.write(f"{hx:.17e} {hy:.17e} {hz:.17e} {J1:.17e} {J2:.17e} {Dval:.17e}\n")
    print(f"Nematic order D = {Dval:.16f}")

    # Chirality
    chirality_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Chirality"))
    os.makedirs(chirality_dir, exist_ok=True)
    chir_file = os.path.join(
        chirality_dir,
        f"Chirality_{N}_{J1_rounded}_{J2_rounded}_{hx_rounded}_{hy_rounded}_{hz_rounded}.dat"
    )

    Sz_r = sr - 0.5
    Sz_rx = srx - 0.5
    Sz_rz = srz - 0.5

    q1 = n_indices ^ (1 << rx)
    SzSx_x = 0.5 * Sz_r * np.real(np.conj(psi[q1]) * psi)

    q2 = n_indices ^ (1 << r)
    SxSz_x = 0.5 * Sz_rx * np.real(np.conj(psi[q2]) * psi)

    Xx = np.sum(SzSx_x - SxSz_x)

    q3 = n_indices ^ (1 << rz)
    SzSx_z = 0.5 * Sz_r * np.real(np.conj(psi[q3]) * psi)

    q4 = n_indices ^ (1 << r)
    SxSz_z = 0.5 * Sz_rz * np.real(np.conj(psi[q4]) * psi)

    Xz = np.sum(SzSx_z - SxSz_z)
    Xavg = 0.5 * (Xx + Xz)

    with open(chir_file, "w") as f_chir:
        f_chir.write(
            f"{hx:.17e} {hy:.17e} {hz:.17e} {J1:.17e} {J2:.17e} "
            f"{abs(Xx):.17e} {abs(Xz):.17e} {abs(Xavg):.17e}\n"
        )
    print(f"Xx = {Xx:.16f}  Xz = {Xz:.16f}  Xavg = {Xavg:.16f}")

    # Magnetization Sx
    mag_sx_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Magnetization", "Sx"))
    os.makedirs(mag_sx_dir, exist_ok=True)
    mag_sx_file = os.path.join(
        mag_sx_dir,
        f"Sx_{N}_{J1_rounded}_{J2_rounded}_{hx_rounded}_{hy_rounded}_{hz_rounded}.dat"
    )

    total_sx = 0.0
    for k in range(N):
        q_k = n_indices ^ (1 << k)
        local_sx = 0.5 * np.real(np.conj(psi[q_k]) * psi)
        total_sx += np.sum(local_sx)
    total_sx_density = total_sx / N

    with open(mag_sx_file, "w") as f_sx:
        f_sx.write(f"{hx:.17e} {hy:.17e} {hz:.17e} {J1:.17e} {J2:.17e} {total_sx_density:.17e}\n")
    print(f"Sx average density = {total_sx_density:.16f}")

    # Magnetization Sz
    mag_sz_dir = os.path.normpath(os.path.join(base_dir, "..", "Data", "Magnetization", "Sz"))
    os.makedirs(mag_sz_dir, exist_ok=True)
    mag_sz_file = os.path.join(
        mag_sz_dir,
        f"Sz_{N}_{J1_rounded}_{J2_rounded}_{hx_rounded}_{hy_rounded}_{hz_rounded}.dat"
    )

    total_sz_weight = 0.0
    for i in range(N):
        total_sz_weight += ((n_indices >> i) & 1) - 0.5
    total_sz_density = np.sum(total_sz_weight * prob) / N

    with open(mag_sz_file, "w") as f_sz:
        f_sz.write(f"{hx:.17e} {hy:.17e} {hz:.17e} {J1:.17e} {J2:.17e} {total_sz_density:.17e}\n")
    print(f"Sz average density = {total_sz_density:.16f}")

if __name__ == "__main__":
    main()
