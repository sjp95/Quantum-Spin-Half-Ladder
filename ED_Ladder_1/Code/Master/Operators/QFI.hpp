#ifndef QFI_HPP_INCLUDED
#define QFI_HPP_INCLUDED

#include "../input.hpp"
#include <Eigen/Dense>
#include <vector>
#include <cmath>
#include <complex>
#include <omp.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include "../creat_directory.hpp"

using namespace std;
using namespace Eigen;

//================================================//
// Quantum Fisher Information for ladder geometry
//
// Generator:
// O(qx) = sum_{x,y} Sz(x,y) exp(-i qx x)
//
// Site mapping:
// x = site / 2
// y = site % 2
//================================================//

void input::QFI(double qx)
{
    createDirectory("../Data/QFI");

    //------------------------------------------------------------
    std::string outfile =
        "../Data/QFI/QFI_" +
        std::to_string(N) + "_" +
        std::to_string(static_cast<int>(std::round(J1 * 100.0))) + "_" +
        std::to_string(static_cast<int>(std::round(J2 * 100.0))) + "_" +
        std::to_string(static_cast<int>(std::round(hx * 100.0))) + "_" +
        std::to_string(static_cast<int>(std::round(hy * 100.0))) + "_" +
        std::to_string(static_cast<int>(std::round(hz * 100.0))) + "_" +
        std::to_string(static_cast<int>(std::round(T * 100.0))) + ".dat";

    std::ofstream file(outfile);
    file << std::scientific << std::setprecision(17);
    //------------------------------------------------------------

    const complex<double> II(0.0, 1.0);

    std::vector<complex<double>> Oq(le, complex<double>(0.0, 0.0));

    double Z = 0.0;
    double beta = 1.0 / T;

    //------------------------------------------------------------
    // Build diagonal operator O(qx) in computational basis
    //------------------------------------------------------------
    #pragma omp parallel for reduction(+:Z)
    for (int state = 0; state < le; state++)
    {
        int n = state;
        complex<double> local(0.0, 0.0);

        for (int site = 0; site < N; site++)
        {
            int reminder = n % Ls;
            n /= Ls;

            double sz = reminder - 0.5;

            int x = site / 2;

            local += sz * exp(-II * qx * double(x));
        }

        Oq[state] = local;

        Z += exp(-(es(state) - es(0)) * beta);
    }

    //------------------------------------------------------------
    // Thermal QFI
    //------------------------------------------------------------
    double QFI_sum = 0.0;

    #pragma omp parallel for reduction(+:QFI_sum) schedule(dynamic)
    for (int l1 = 0; l1 < le; l1++)
    {
        for (int l2 = l1 + 1; l2 < le; l2++)
        {
            double p1 = exp(-(es(l1) - es(0)) * beta);
            double p2 = exp(-(es(l2) - es(0)) * beta);

            double numerator = (p1 - p2) * (p1 - p2);
            double denominator = p1 + p2;

            if (denominator < 1e-14)
                continue;

            if (numerator / denominator < 1e-12)
                continue;

            complex<double> matrix_element(0.0, 0.0);

            for (int state = 0; state < le; state++)
            {
                matrix_element +=
                    Oq[state] *
                    conj(evs(state, l1)) *
                    evs(state, l2);
            }

            QFI_sum +=
                4.0 *
                norm(matrix_element) *
                numerator / denominator;
        }
    }

    double qfi_density = QFI_sum / (double(N) * Z);

    cout << "QFI = " << qfi_density << endl;

    file << T << " "
         << hz << " "
         << J1 << " "
         << J2 << " "
         << qfi_density << endl;

    file.close();
}

#endif
