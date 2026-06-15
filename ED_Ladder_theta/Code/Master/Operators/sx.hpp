#ifndef SX_HPP_INCLUDED
#define SX_HPP_INCLUDED
#include "../input.hpp"
#include <Eigen/Dense>
#include <omp.h>
using namespace std;
using namespace Eigen;

//============================================================================================//
                        //=== Aveg <O> calculation ===//
//============================================================================================//

// void input::gSxig( int i)
// {
//     int n = i;
//     for(int k1=0; k1<N; k1++)
//     {
//         long long bi1=0;
//         int id=0;
//         for ( int j =0; j<N; j++)
//         {
//             int reminder = i%Ls;
//             i=i/Ls;
//             //======================//
//             if(j==k1)
//             {
//                  if (reminder<Ls-1)
//                 {
//                     reminder+=1;
//                     id++;
//                 }
//                 else
//                 {
//                     reminder-=1;
//                     id++;
//                 }
//             }
//             //======================//
//             bi1+=reminder*pow(Ls,j);
//             //=======================//
//         }
//         //======================================//
//         double sss=double(id);
//         int q =int(bi1);// Decimal(bi1);
//         if(q!=n)
//         O(k1)+=conj(evs(q,0))*evs(n,0)*sss;
//         //======================================//
//         i=n;
//     }
// }

//  void input::Sx()
//  {
//      VectorXcd sxi = VectorXcd :: Zero(N);
//      bool tut=createDirectory("../Data/Sx/");
//     std::string outfile ="../Data/Sx/EigenSpectrum_" + std::to_string(N) + "_" +    std::to_string(int(J1*100.0)) + "_" +    std::to_string(int(J2*100.0)) + "_" +    std::to_string(int(hz*100.0)) +  ".h5";
//         ofstream file(outfile);

//      #pragma omp parallel for
//      for(int i=0;i<le;i++)
//      {
//          gSxig(i);
//      }
      
//      double O=0.0;
//      for(int i=0;i<N;i++)
//      {
//         //  B(i,i)=complex<double>(O(i));
//             O+=sxi(i).real();
            
//      }
//      file << hz<<" "<<J1<<" "<<J2<<" "<< sxi(i).real() << " "<<O/double(N)<< endl;
//  }


//========================================================================================//
//========================================================================================//
// void input::Sx()
// {
//     createDirectory("../Data/Magnetization/Sx");
    
//     //------------------------------------------------//
//     std::string outfile =
//         "../Data/Magnetization/Sx/Sx_" +
//         std::to_string(N) + "_" +
//         std::to_string(int(J1*100.0)) + "_" +
//         std::to_string(int(J2*100.0)) + "_" +
//         std::to_string(int(hz*100.0)) + ".dat";

//     std::ofstream file(outfile);
//     //------------------------------------------------//

//     VectorXcd sxi = VectorXcd::Zero(N);

//     #pragma omp parallel
//     {
//         VectorXcd local_sxi = VectorXcd::Zero(N);

//         #pragma omp for schedule(static)
//         for(int n = 0; n < le; n++)
//         {
//             for(int k1 = 0; k1 < N; k1++)
//             {
//                 int state = n;
//                 long long bi1 = 0;
//                 double factor = 0;
//                 int mult = 1;

//                 for(int j = 0; j < N; j++)
//                 {
//                     int reminder = state % Ls;
//                     state /= Ls;

//                     if(j == k1)
//                     {
//                         if(reminder < Ls-1)
//                             reminder++;
//                         else
//                             reminder--;

//                         factor = 1;
//                     }

//                     bi1 += reminder * mult;
//                     mult *= Ls;
//                 }

//                 int q = int(bi1);

//                 if(q != n)
//                     local_sxi(k1) += conj(evs(q,0))*evs(n,0)*factor;
//             }
//         }

//         #pragma omp critical
//         sxi += local_sxi;
//     }

//     double total = sxi.real().sum();

//     file << hz << " "
//          << J1 << " "
//          << J2 << " "
//          << total << endl;
// }

//========================================================================================//
//========================================================================================//
void input::Sx()
{
    createDirectory("../Data/Magnetization/Sx");

    std::string outfile =
    "../Data/Magnetization/Sx/Sx_" +
    std::to_string(N) + "_" +
    std::to_string(static_cast<int>(std::round(theta * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hx * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hy * 100.0))) + "_" +
    std::to_string(static_cast<int>(std::round(hz * 100.0))) + ".dat";

    std::ofstream file(outfile);
    file << std::scientific << std::setprecision(17);

    const auto* psi = evs.col(0).data();

    double total = 0.0;

    #pragma omp parallel for reduction(+:total) schedule(static)
    for(int n = 0; n < le; n++)
    {
        std::vector<int> spin(N);

        int temp = n;

        for(int j=0;j<N;j++)
        {
            spin[j] = temp % Ls;
            temp /= Ls;
        }

        double local = 0.0;

        for(int k=0;k<N;k++)
        {
            int q = n;

            if(spin[k] == 0)
                q += Lspow[k];
            else
                q -= Lspow[k];

            local += std::real(std::conj(psi[q]) * psi[n]) * 0.5;
        }

        total += local;
    }

    file << hx << " "
            << hy << " "
            << hz << " "
            << theta << " "
            << total/double(N)
            << std::endl;
}
//========================================================================================//
//========================================================================================//

#endif