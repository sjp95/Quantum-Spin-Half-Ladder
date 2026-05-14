#ifndef Sz_HPP_INCLUDED
#define Sz_HPP_INCLUDED
#include "../input.hpp"
#include <Eigen/Dense>
#include <omp.h>
using namespace std;
using namespace Eigen;

//



void input::Sz()
{
    createDirectory("../Data/Magnetization/Sz");
    
    //------------------------------------------------//
    std::string outfile =
    "../Data/Magnetization/Sz/Sz_" +
    std::to_string(N) + "_" +
    std::to_string(static_cast<int>(std::round(J1 * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(J2 * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hz * 100.0))) + ".dat";

    std::ofstream file(outfile);
    file << std::scientific << std::setprecision(17);
    //------------------------------------------------//

    double total = 0.0;

    #pragma omp parallel for reduction(+:total) schedule(static)
    for (int n = ls; n < le; n++)
    {
        int state = n;
        double weight = std::norm(evs(n,0));
        double local = 0.0;

        for (int i = 0; i < N; i++)
        {
            int reminder = state % Ls;
            state /= Ls;
            local += (reminder - 0.5);
        }

        total += local * weight;
        //cout << "State: " << n << ", Local Sz: " << local << ", Weight: " << weight << endl;
    }
   
    
    file << hz << " "
         << J1 << " "
         << J2 << " "
         << total/double(N) << endl;
}
//================================================//
//================================================//
#endif