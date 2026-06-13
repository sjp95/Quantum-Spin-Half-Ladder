#include <iostream>
#include <cmath>
#include <math.h> 
#include <complex>
#include <fstream>
//#include <omp.h>
//#include "mkl_lapacke.h"
#include "Master/master.hpp"
using namespace std;

char title[100];

int main(int argc,char* argv[])
{
    // std::ofstream file;               //| ==== File | L
    // file.open("U-phi.dat");

    int N=atoi(argv[1]);
    double T=atof(argv[2]);
    double J1=atof(argv[3])/100.0;
    double J2=atof(argv[4])/100.0;
    double hx=atof(argv[5])/100.0;
    double hy=atof(argv[6])/100.0;
    double hz=atof(argv[7])/100.0;

    input Data;
    Data.T=T;
    Data.J1=J1;
    Data.J2=J2;
    Data.hx=hx;
    Data.hy=hy;
    if(argc > 8)
    {
        Data.bc = argv[8];
    }
    else
    {
        Data.bc = "obc";
    }
    Data.besis(N,J1,J2,hx,hy,hz);
   // Data.Values();
    Data.mu_phi();
    
    
}



//===============================================================//
//==============================================================//
// for (double i = 0; i <= 100; i+=1)
// {
//     Data.U_phi(i/10.0);
//     file<< i/10.0<<"    "<<Data.O.transpose().real()<<endl;
// }

//int i=atof(argv[1]);
// int u=i-8;

// sprintf(title,"U-phi.dat"); //| ==== Name | I
// std::ofstream file(title, std::fstream::out | std::fstream::app); 
// {
//     Data.mu_phi();
//     //file<< u<<"    "<<Data.O.transpose().real()<<endl;
//     file<<"\n"<<endl;
// }


// sprintf(title,"U-phi.dat"); //| ==== Name | I
// std::ofstream file(title, std::fstream::out | std::fstream::app); 
// {
//     Data.U_phi(i/10.0);
//     file<< i/10.0<<"    "<<Data.O.transpose().real()<<endl;
//     file<<"\n"<<endl;
// }



//file.close();
//==============================================================//
//==============================================================//