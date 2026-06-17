#ifndef CHIRALITY_HPP_INCLUDED
#define CHIRALITY_HPP_INCLUDED

#include "../input.hpp"
#include <Eigen/Dense>
#include <omp.h>

using namespace std;
using namespace Eigen;

void input::Chirality()
{
    createDirectory("../Data/Chirality");

    std::string outfile =
    "../Data/Chirality/Chirality_" +
    std::to_string(N) + "_" +
    std::to_string(static_cast<int>(std::round(J1*100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(J2*100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hx*100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hy*100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hz*100.0))) +
    ".dat";

    std::ofstream file(outfile);
    file << scientific << setprecision(17);

    const auto* psi = evs.col(0).data();

    double Xx = 0.0;
    double Xz = 0.0;

    int Nx = N/2;

    #pragma omp parallel for reduction(+:Xx,Xz)
    for(int n=0;n<le;n++)
    {
        double localXx = 0.0;
        double localXz = 0.0;

        for(int r=N/2;r<N/2+1;r++)
        {
            int x = r/2;
            int y = r%2;

            int xp = (x+1)%Nx;
            int yp = (y+1)%2;

            int rx = xp*2 + y;
            int rz = x*2 + yp;

            //------------------------------------
            // spins
            //------------------------------------

            int sr  = (n/Lspow[r ])%2;
            int sxb = (n/Lspow[rx])%2;
            int szb = (n/Lspow[rz])%2;

            double Sz_r  = sr  - 0.5;
            double Sz_rx = sxb - 0.5;
            double Sz_rz = szb - 0.5;

            //------------------------------------
            // Sz(r)Sx(rx)
            //------------------------------------

            int q1 = n;

            q1 += (1-2*sxb)*Lspow[rx];

            double SzSx_x =
            0.5*Sz_r*
            std::real(std::conj(psi[q1])*psi[n]);

            //------------------------------------
            // Sx(r)Sz(rx)
            //------------------------------------

            int q2 = n;

            q2 += (1-2*sr)*Lspow[r];

            double SxSz_x =
            0.5*Sz_rx*
            std::real(std::conj(psi[q2])*psi[n]);

            //------------------------------------
            // Xx bond
            //------------------------------------

            localXx +=
            (SzSx_x - SxSz_x);

            //------------------------------------
            // Sz(r)Sx(rz)
            //------------------------------------

            int q3 = n;

            q3 += (1-2*szb)*Lspow[rz];

            double SzSx_z =
            0.5*Sz_r*
            std::real(std::conj(psi[q3])*psi[n]);

            //------------------------------------
            // Sx(r)Sz(rz)
            //------------------------------------

            int q4 = n;

            q4 += (1-2*sr)*Lspow[r];

            double SxSz_z =
            0.5*Sz_rz*
            std::real(std::conj(psi[q4])*psi[n]);

            //------------------------------------
            // Xz bond
            //------------------------------------

            localXz +=
            (SzSx_z - SxSz_z);
        }

        Xx += localXx;
        Xz += localXz;
    }

    double Xavg = 0.5*(Xx + Xz);

    file
    << hx << " "
    << hy << " "
    << hz << " "
    << J1 << " "
    << J2 << " "
    << std::abs(Xx) << " "
    << std::abs(Xz) << " "
    << std::abs(Xavg)
    << std::endl;

    std::cout
    << "Xx = " << Xx
    << "  Xz = " << Xz
    << "  Xavg = " << Xavg
    << std::endl;
}

#endif