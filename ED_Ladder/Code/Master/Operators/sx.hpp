#ifndef O_HPP_INCLUDED
#define O_HPP_INCLUDED
#include "../input.hpp"
#include <Eigen/Dense>
#include <omp.h>
using namespace std;
using namespace Eigen;

//============================================================================================//
                        //=== Aveg <O> calculation ===//
//============================================================================================//

void input::phi( int i)
{
    int n = i;
    for(int k1=0; k1<N; k1++)
    {
        long long bi1=0;
        int id=0;
        for ( int j =0; j<N; j++)
        {
            int reminder = i%Ls;
            i=i/Ls;
            //======================//
            if(j==k1)
            {
                 if (reminder<Ls-1)
                {
                    reminder+=1;
                    id++;
                }
            }
            //======================//
            bi1+=reminder*pow(Ls,j);
            //=======================//
        }
        //======================================//
        double sss=double(id);
        int q =int(bi1);// Decimal(bi1);
        if(q!=n)
        O(k1)+=conj(evs(q,0))*evs(n,0)*sss;
        //======================================//
        i=n;
    }
}

 void input::OO()
 {
     O = VectorXcd :: Zero(N);
     #pragma omp parallel for
     for(int i=0;i<le;i++)
     {
         phi(i);
     }

     for(int i=0;i<N;i++)
     {
         B(i,i)=complex<double>(O(i));
     }
 }


//========================================================================================//
//========================================================================================//

#endif