#ifndef NSCINPUT_HPP_INCLUDED
#define NSCINPUT_HPP_INCLUDED
#include "math.h"
#include <complex>
#include <Eigen/Dense>
#include <vector>
#include <chrono>
#include <fftw3.h>
#include <string>
using namespace std;
using namespace Eigen;
//=======================================================//
class NSC_input
{
    public:
        int N=12;
        int nup=6;
        int ndown=0;
        int ttt0=0;
        int ttt1=0;
        int jjt0=0;
        int jjt1=0;
        int hz=0;
        double etamultiplyer=0.0;
        bool createDirectory(const std::string& path);
        std::string argument = "FFTW";
    private:
        
        //=========================================================//
                         //====Basis formation====//
        //=========================================================//
        long long fact(long long n);         
        long long nCr(long long n,long long r); 
        double delta(double x0, double x);    
        void fftShift(fftw_complex* data, int size);

        void order0_data();        
        void Sq0();            

        void order1_data();        
        void Sq1();       

        void order2_data();        
        void Sq2();       
        // vector<int> basisarray;
        // int find(int target);//====An algorithm to find location of a number====//
        //=========================================================//
                      //====Hamiltonian formation====//
        //=========================================================//
        
    public:
        void Consolidet_NSC();
        void Data_of_order(int ii);
       
    
        
};

//=========================================================//
//=========================================================//
long long NSC_input::fact(long long n)
{
  if (n == 0 || n == 1)
  return 1;
  else
  return n * fact(n - 1);
}
//=========================================================//
long long NSC_input:: nCr(long long n,long long r)
{
  if(n>=r)
  {
      return fact(n) / (fact(r) * fact(n - r));
  }
  else
  {
      return 0;
  }
}
//=========================================================//
//=========================================================//


// //======================================================//
// double NSC_input:: Fermi(double e,double m)
// { 
//     return 1/(exp((e-m)/T)+1);
// }
// //=======================================================//
double NSC_input::delta(double x0, double x)
{
    double L=0.15;
    double D= (L/(2*M_PI))/(0.01+(x-x0)*(x-x0));
    return D;
}
// //=======================================================//
// void NSC_input:: Partition_function()
// { 
//     Z=0.0;
//     for(int i=0;i<es.size();i++)
//     {
//         Z+=exp(-(es(i)-es(0))/T);
//     }
// }
// //======================================================//
#endif