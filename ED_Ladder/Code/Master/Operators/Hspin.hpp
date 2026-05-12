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
complex<double> input::diagonal(int n)
{
    complex <double> D=complex <double>(0,0);
    VectorXcd nnt = VectorXcd :: Zero(N);
    //int m = n;
    
    for ( int i =0; i<N; i++)
    {
        double reminder = n%Ls;
        n=n/Ls;
        double nt = double(reminder-1.0/2.0);
        nnt(i)=complex<double>(nt,0.0);
        D+=- hz*nt;
    }
    //cout<< D <<endl;
    for (int i = 0; i < N; i++)
    {
        for (int j = i+1; j < N; j++)
        if(abs(Jz(i,j))>0)
        {
            D+= Jz(i,j)* nnt(i)* nnt(j);
        }
    }
    //std::cout<< m <<"  |"<< nnt.transpose()<<">  "<<D<<endl;
    //cout<< D <<endl;
    
    return D;
}


//================================================//
          //=== Hamiltonian Formation ===//
//================================================//
void input::Hspin()
{
    H= MatrixXcd :: Zero(le,le);
    //#pragma omp parallel for
    //omp_set_num_threads(4);
    #pragma omp parallel for
    for (int i =ls ; i< le; i++)
    {
         H(i,i) = diagonal(i);
         insidehoping(i);    
        // outsidehoping(i);
    }
   
}
//================================================//
//================================================//
#endif


