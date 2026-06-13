#ifndef HSPIN_HPP_INCLUDED
#define HSPIN_HPP_INCLUDED
#include "../input.hpp"
#include <Eigen/Dense>
//#define EIGEN_USE_MKL_ALL
#include <omp.h>
#include "inside.hpp"
#include "outside.hpp"
using namespace std;
using namespace Eigen;


//================================================//
            //=== Diagonal element ===//
//================================================//
// complex<double> input::diagonal(int n)
// {
//     complex <double> D=complex <double>(0,0);
//     VectorXcd nnt = VectorXcd :: Zero(N);
//     //int m = n;
    
//     for ( int i =0; i<N; i++)
//     {
//         double reminder = n%Ls;
//         n=n/Ls;
//         double nt = double(reminder-1.0/2.0);
//         nnt(i)=complex<double>(nt,0.0);
//         D+=- hz*nt;
//     }
//     //cout<< D <<endl;
//     for (int i = 0; i < N; i++)
//     {
//         for (int j = i+1; j < N; j++)
//         if(abs(Jz(i,j))>0)
//         {
//             D+= Jz(i,j)* nnt(i)* nnt(j);
//         }
//     }
//     //std::cout<< m <<"  |"<< nnt.transpose()<<">  "<<D<<endl;
//     //cout<< D <<endl;
    
//     return D;
// }

complex<double> input::diagonal(int state)
{
    double D = 0.0;
    std::vector<double> spin(N);

    for (int i = 0; i < N; i++)
    {
        int reminder = state % Ls;
        state /= Ls;

        double nt = reminder - 0.5;
        spin[i] = nt;

        D += -hz * nt;
    }

    for (int i = 0; i < N; i++)
    {
        for (int j = i + 1; j < N; j++)
        {
            if (Jz(i,j) != 0.0)
                D += Jz(i,j).real() * spin[i] * spin[j];
        }
    }

    return complex<double>(D, 0.0);
}

//================================================//
          //=== Hamiltonian Formation ===//
//================================================//
// void input::Hspin()
// {
//     H= MatrixXcd :: Zero(le,le);
//     //#pragma omp parallel for
//     //omp_set_num_threads(4);
//     #pragma omp parallel for
//     for (int i =ls ; i< le; i++)
//     {
//          H(i,i) = diagonal(i);
//          insidehoping(i);    
//         // outsidehoping(i);
//     }
   
// }

// void input::Hspin()
// {
//     H = MatrixXcd::Zero(le, le);

//     #pragma omp parallel for schedule(dynamic)
//     for(int i=ls; i<le; i++)
//     {
//         H(i,i) = diagonal(i);
//         insidehoping(i);
//     }

//     //H = H.selfadjointView<Eigen::Upper>();
// }
//================================================//
//================================================//
void input::Hspin()
{
    H = MatrixXcd::Zero(le, le);
    int Nx = N/2; // Assuming a 2D lattice with 2 sites in the x-direction

    #pragma omp parallel for schedule(static)
    for(int state = ls; state < le; state++)
    {
        std::vector<int> spin(N);

        int temp = state;
        double diag = 0.0;

        for(int i=0;i<N;i++)
        {
            spin[i] = temp % Ls;
            temp /= Ls;

            double sz = spin[i] - 0.5;
            diag -= hz * sz;
        }

        for(int i=0;i<N;i++)
        {
            for(int j=i+1;j<N;j++)
            {
                if(Jz(i,j).real() != 0.0)
                {
                    double si = spin[i] - 0.5;
                    double sj = spin[j] - 0.5;
                    diag += Jz(i,j).real() * si * sj;
                }
            }
        }

        H(state,state) = diag;

        for(int k1=0;k1<N;k1++)
        {
            //======================================//
            int x = k1/2;
            int y = k1%2;

            int xp  = (x+1)%Nx;
            int yp  = (y+1)%2;

            int kxp = xp*2 + y;
            int kyp = x*2 + yp;
            int kxyp = xp*2 + yp;
            //======================================//
            //for(int k2=k1+1;k2<N;k2++)
            // if(abs(Jx(k1,k2).real()) > 0.0 )
            // {
                // if(Jx(k1,k2).real() == 0.0)
                //     continue;

                int q = state;

                //q = q + (spin[k1] == 0 ? Lspow[k1] : -Lspow[k1]);
                //q = q + (spin[k2] == 0 ? Lspow[k2] : -Lspow[k2]);

                q = q + (1 - 2*spin[k1]) * Lspow[k1]; // Spin half only
                q = q + (1 - 2*spin[kxp]) * Lspow[kxp]; // Spin half only
                q = q + (1 - 2*spin[kyp]) * Lspow[kyp]; // Spin half only
                q = q + (1 - 2*spin[kxyp]) * Lspow[kxyp]; // Spin half only

                if(q != state && q > state)
                {
                   H(state,q) += 0.25* 0.25* Jx(k1,kxp)*0.5;
                }
            //}
           //======================================//
                // hx, hy terms
           //======================================//
            int q1 = state;
            //int q = state + (spin[k1] == 0 ? Lspow[k1] : -Lspow[k1]);
            q1 = state + (1 - 2*spin[k1]) * Lspow[k1]; // Spin half only

            //cd amp = cd(0.0, (spin[k1] == 0 ? -0.5*hy : 0.5*hy));
            //cd amp(0.0, 0.5 * hy * (2*spin[k1] - 1));
            
            if(q1 != state && q1 > state)
            {
                H(state,q1) += -0.5 * hx;
            }
            //======================================//
        }
    }

    H = H.selfadjointView<Eigen::Upper>();
}
#endif


