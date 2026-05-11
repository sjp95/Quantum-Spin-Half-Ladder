#ifndef VALUES_HPP_INCLUDED
#define VALUES_HPP_INCLUDED
#include <math.h>
#include "input.hpp"
#include <Eigen/Dense>

#include <complex>
using namespace Eigen;
using namespace std;

//=================== General input ====================//


void input::Values()
{

   Jx= MatrixXcd:: Zero(N,N);
   Jz= MatrixXcd:: Zero(N,N);
    for (int k=0;k<N;k++) //| === Basis loop (site basis)
    {
       int Nx=N/2;
       int x=k/2;
       int y=k%2;
       int xp=(x+1)%Nx; 
       int yp=(y+1)%2;
       int kxp=xp*2+y;
       int kyp=x*2+yp;
       if(x<Nx-1)
       {
           Jx(k,kxp)=J1;
           Jx(kxp,k)=J1;
       }
       Jz(k,kyp)=J2;
       Jz(kyp,k)=J2;
    }

    cout<< "==============================="<<endl;
    cout<< "Hoping Generated"<<endl;
    cout<< "==============================="<<endl;

}
//======================================================//

#endif
