#include <iostream>
#include <cmath>
#include <math.h> 
#include <complex>
#include <fstream>
#include <omp.h>
#include "Data/NSC/NSCorder.hpp"
#include "Data/NSC/consolidate.hpp"

#include "Data/SC/SCorder.hpp"
#include "Data/SC/consolidate.hpp"
// #include "t-J/master.hpp"
// #include "t-J/input/creat_directory.hpp"
// #include "t-J/Operator/operators.hpp"
// #include "t-J/Operator/pobopp.hpp"

using namespace std;

int main(int argc,char* argv[])
{
    int N=atoi(argv[1]);
    int nup=atoi(argv[2]);
    int ndown=atoi(argv[3]);
    int ttt0=atoi(argv[4]);
    int ttt1=atoi(argv[5]);
    int jjt0=atoi(argv[6]);
    int jjt1=atoi(argv[7]);
    double eta=atof(argv[8]);
    int hz=atoi(argv[10]);

    
    
    //===========================//
    //===========================//
    NSC_input Data1;
    Data1.N=N;
    Data1.nup=nup;
    Data1.ndown=ndown;
    Data1.ttt0=ttt0;
    Data1.ttt1=ttt1;
    Data1.jjt0=jjt0;
    Data1.jjt1=jjt1;
    Data1.hz=hz;
    Data1.etamultiplyer=eta;
    Data1.argument = "c++";
    //Data1.argument = "FFTW"; //default


    // SC_input Data;
    // Data.N=N;
    // Data.nup=nup;
    // Data.ndown=ndown;
    // Data.ttt0=ttt0;
    // Data.ttt1=ttt1;
    // Data.jjt0=jjt0;
    // Data.jjt1=jjt1;
    // Data.etamultiplyer=eta;
    //Data.argument = "c++";
    //Data.argument = "FFTW"; //default

    if(strcmp(argv[9], "c") == 0)
    {
        Data1.Consolidet_NSC();
        //Data.Consolidet_SC();
    }
    else
    {
        int order=atoi(argv[9]);
        Data1.Data_of_order(order);
        //Data.Data_of_order(order);
    }
    
   
    //===========================//
    //===========================//
    

    //operators_NSC alpha;
    //Data1.Hamiltonian();
    
}
