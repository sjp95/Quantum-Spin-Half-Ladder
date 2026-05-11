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
#include <math.h> 
#include <complex>
#include <fstream>
#include <vector>
#include "../creat_directory.hpp"
using namespace std;
using namespace Eigen;


//================================================//
            //=== QFI ===//
//================================================//


void input::QFI(double q)
{ 
    std::vector<complex<double>> SZZ(le, std::complex<double>(0.0, 0.0));
    complex <double> II=complex <double>(0,1.0);

    double ZZ=0.0;

    omp_set_num_threads(4);
    #pragma omp parallel for
    for ( int i =0; i<le; i++)
    {
        int n=i;
        for ( int j =0; j<N; j++)
        {
            double reminder = n%Ls;
            n=n/Ls;
            double nt = double(reminder-1.0/2.0);
            SZZ[i]+= nt*exp(-II*q*double(j));
        }
       // cout<< i<<" "<<SZZ[i].real() <<endl;
       ZZ+=abs(exp(-(es(i)-es(0)) / T));
    }

    double QFI_sum_re = 0.0;
    double QFI_sum_im = 0.0;

    //------------------------------------------------------------------------------------------
    char title0[150];
    //------------------------------------------------------------------------------------------
    bool tut=createDirectory("../Data");
         tut=createDirectory("../Data/QFI");
    sprintf(title0,"../Data/QFI/QFI_%d_%d_%d_%d.dat",N,int(J1*100.0),int(J2*100.0),int(T*100.0));
    std::ofstream file0;               //| ==== File | L
    file0.open(title0);                //| ==== Open | E
    file0 << std::fixed << std::setprecision(16);
    //-------------------------------------------------------------------------------------------
    // double QFI_sum_re = 0.0;
    // double QFI_sum_im = 0.0;
    //==========================================================================================
    // #pragma omp parallel for reduction(+:QFI_sum_re, QFI_sum_im)
    // for (int l1 = 0; l1 < le; l1++)
    // {
    
    //     for (int l2 = l1+1; l2 < le; l2++)
    //     {
    //         // if(abs(pow(exp(-(es(l1)-es(0))/T) - exp(-(es(l2)-es(0))/T), 2.0)/(exp(-(es(l1)-es(0))/T) + exp(-(es(l2)-es(0))/T)))<0.000001)
    //         // {
    //             complex<double> element_QFI(0.0,0.0);
    //             for (int i = 0; i < le; i++)
    //             {
    //                 element_QFI += SZZ[i] * conj(evs(i,l1)) * evs(i,l2);
    //             }

    //             complex<double> contrib =4.0 *pow(abs(element_QFI), 2.0) * pow((exp(-(es(l1)-es(0))/T) - exp(-(es(l2)-es(0))/T)), 2.0)/(exp(-(es(l1)-es(0))/T) + exp(-(es(l2)-es(0))/T));
    //             //complex<double> contrib =2.0 *pow(abs(element_QFI), 2.0) * pow(exp(-(es(l1))/T) - exp(-(es(l2))/T), 2.0)/(exp(-(es(l1))/T) + exp(-(es(l2))/T));            

    //             QFI_sum_re += contrib.real();
    //             QFI_sum_im += contrib.imag();
    //         //}
    //     }
    // }
    //==========================================================================================
        double QFI_sum = 0.0;
        double beta = 1.0 / T;

        #pragma omp parallel for reduction(+:QFI_sum)
        for (int l1 = 0; l1 < le; l1++)
        {
            for (int l2 = l1+1; l2 < le; l2++)
            {

                double e1 = abs(exp(-(es(l1)-es(0)) * beta));
                double e2 = abs(exp(-(es(l2)-es(0)) * beta));

                double boltz = pow((e1 - e2),2);
                double denom = (e1 + e2);

                if(abs(boltz / denom)>0.00001)
                {
                    std::complex<double> element_QFI(0.0,0.0);

                    for (int i = 0; i < le; i++)
                    {
                        element_QFI += SZZ[i] * std::conj(evs(i,l1)) * evs(i,l2);
                    }

                
                    double contrib = 4.0 * std::norm(element_QFI) * boltz / denom;
                
        //            cout<< boltz<<"    "<<denom<<"  "<<boltz / denom<<"     "<<norm(element_QFI)<<endl;

                    QFI_sum += contrib;
                }
            }
        }
    //===========================================================================================


    //complex<double> QFI_sum(QFI_sum_re, QFI_sum_im);
    cout << "QFI_sum: " << QFI_sum/(double(N)*ZZ) << endl;
    //file0 << T <<"      "<<QFI_sum.real()/double(N) << endl;
    file0 << T <<"      "<<QFI_sum/(double(N)*ZZ) << endl;
    
    
    file0.close();
    
}

#endif
