#ifndef D_HPP_INCLUDED
#define D_HPP_INCLUDED

#include "../input.hpp"
#include <Eigen/Dense>
#include <omp.h>

using namespace std;
using namespace Eigen;

//================================================//
// Nematic order parameter
//
// D = Σ_r [ σx_r σx_{r+x}
//          -σz_r σz_{r+z} ]
//
// σ = 2S
//
// D = 4 Σ_r [ SxSx - SzSz ]
//
//================================================//

void input::D()
{
    //========================================================================//
    createDirectory("../Data/Nematic");

    std::string outfile =
    "../Data/Nematic/D_" +
    std::to_string(N) + "_" +
    std::to_string(static_cast<int>(std::round(J1 * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(J2 * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hx * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hy * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hz * 100.0))) +
    ".dat";

    std::ofstream file(outfile);
    file << std::scientific << std::setprecision(17);
    //========================================================================//
    const auto* psi = evs.col(0).data();

    double Dval = 0.0;

    int Nx = N/2;
    //========================================================================//
    #pragma omp parallel for reduction(+:Dval) schedule(static)
    for(int n=0;n<le;n++)
    {
        double prob = std::norm(psi[n]);

        double local = 0.0;

        for(int r=N/2;r<N/2+1;r++)
        {
            //----------------------------------
            // lattice coordinates
            //----------------------------------

            int x = r/2;
            int y = r%2;

            //----------------------------------
            // neighbors
            //----------------------------------

            int xp = (x+1)%Nx;
            int yp = (y+1)%2;

            int rx = xp*2 + y;   // x-bond
            int rz = x*2 + yp;   // z-bond

            //----------------------------------
            // <Sx_r Sx_rx>
            //----------------------------------

            int sr  = (n/Lspow[r ])%2;
            int srx = (n/Lspow[rx])%2;

            int q = n;

            q += (1-2*sr )*Lspow[r ];
            q += (1-2*srx)*Lspow[rx];

            double sxsx = 0.25*std::real(std::conj(psi[q])*psi[n]);

            //----------------------------------
            // <Sz_r Sz_rz>
            //----------------------------------

            double szr =sr - 0.5;
            double szrz =((n/Lspow[rz])%2)-0.5;

            double szsz =prob*szr*szrz;

            //----------------------------------

            local += 4.0*(sxsx - szsz);
        }

        Dval += local;
    }
    //========================================================================//

    //Dval /= double(N);

    file << hx << " "
         << hy << " "
         << hz << " "
         << J1 << " "
         << J2 << " "
         << Dval
         << std::endl;
    //========================================================================//
    std::cout
    << "Nematic order D = "
    << Dval
    << std::endl;
    //========================================================================//
}

#endif