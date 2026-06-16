# Spin-1/2 Ladder Project

This project studies a spin-($\tfrac{1}{2}$) two-leg ladder system in the presence of an external magnetic field applied along the (z)-direction. The model features anisotropic exchange interactions: the intra-leg coupling acts along the (x)-spin component, while the inter-leg (rung) coupling acts along the (z)-spin component.

The system provides a platform to investigate competing quantum fluctuations and anisotropic correlations, with relevance to quantum magnetism and strongly correlated systems.

Numerical calculations will be performed using the Matrix Product State (MPS) formalism and the Density Matrix Renormalization Group (DMRG) algorithm, implemented in Julia using the ITensor library.


## Hamiltonian

The Hamiltonian of the system is given by:

$$ H = J_{\parallel} \sum_{\langle i,j \rangle \in \text{legs}} S_i^x S_j^x +J_{\perp} \sum_{\langle i,j \rangle \in \text{rungs}} S_i^z S_j^z- h \sum_i S_i^z $$

### Parameters

* `J_parallel` : coupling along the ladder legs (($S^x S^x$))
* `J_perp`     : coupling along the rungs (($S^z S^z$))
* `h`          : external magnetic field along (z)
* ($S_i^\alpha$): spin-($\tfrac{1}{2}$) operators (($\alpha$ = x, y, z))


## Ladder Geometry

The system consists of two coupled one-dimensional chains:

```
Leg 1:   ●───●───●───●───●
         │   │   │   │   │
Leg 2:   ●───●───●───●───●
```

### Legend

* `●` : Spin-1/2 site
* `───` : Leg interaction (($J_{\parallel} S^x_i S^x_j$))
* `│`   : Rung interaction (($J_{\perp} S^z_i S^z_j$))

---

## Physical Picture

* The **leg coupling** (($S^x S^x$)) introduces transverse quantum fluctuations.
* The **rung coupling** (($S^z S^z$)) favors correlations along the (z)-direction.
* The **magnetic field** competes with interactions by polarizing spins.

The interplay of these terms can give rise to nontrivial quantum phases, including anisotropic ordering and field-driven transitions.


## Numerical Approach

* Mapping the ladder to a 1D chain for MPS representation
* Using DMRG to compute:

  * Ground state energy
  * Low-lying excitations
  * Correlation functions
  * Magnetization

## Exact Diagonalisation (C++) Dependency

The exact diagonalisation (ED) code written in C++ uses the **Eigen** linear algebra library.

* Eigen website: https://libeigen.gitlab.io/
* Eigen is header-only and can be included directly in this project.
* Eigen (since v3.1.1) is primarily licensed under **MPL 2.0**.
* If anyone wants to modify any Eigen file, those modified Eigen files must remain under MPL 2.0.

## Future Extensions

* Phase diagram as a function of ($J_{\parallel}, J_{\perp}, h$)
* Entanglement entropy and scaling analysis
* Dynamical properties using time-evolution (tDMRG / TEBD)
* Finite temperature DMRG

## Third-party dependencies

This project vendors the following open-source libraries:

- HighFive (BSD-3-Clause)
  https://github.com/BlueBrain/HighFive.git

- Eigen (MPL 2.0)
  https://eigen.tuxfamily.org



