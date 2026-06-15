#ifndef INPUT_HPP_INCLUDED
#define INPUT_HPP_INCLUDED
#include "math.h"
#include <complex>
#include <Eigen/Dense>
using namespace std;
using namespace Eigen;
//=======================================================//
class input
{
    private:
        int N = 1;                  // Total No of site in cluster    | U
        double U = 8;               // interaction Energy             | E
        double lz = 1.0/2.0;              // Lz                             | F
        int Ls = 2*lz+1;            // Degrees or freedom (2*L+1)     | A
        int le = pow(Ls,N);
                                    // Lattice diamention            | L
        double mus = 0.0;           // chemical potential of Hs       | T
        int ls=0;
        double filling =1;

        // MatrixXcd evss = MatrixXcd :: Zero(le,le);
        // VectorXcd DO_s = VectorXcd :: Zero(N);
        //=================================================================//
        MatrixXcd H = MatrixXcd :: Zero(le,le);
        //MatrixXcd t= MatrixXcd::Ones(N,N);             //             | D 
        MatrixXcd Jx= MatrixXcd::Ones(N,N);             //             | D 
        MatrixXcd Jz= MatrixXcd::Ones(N,N);             //             | D 
        MatrixXcd evs = MatrixXcd :: Zero(le,le);      //             | A
        VectorXd es = VectorXd :: Zero(le);
        //-------------------------------------------------//
        //=================================================================//
    public:               
        double hx=0.0, hy=0.0, hz=0.0;   // Magnetic field components
        double J1=1.0;
        double J2=1.0;
        double t1=0.0;
        double T = 0.1;       // Temperature                    | D
        string bc;
        
        void besis(int NN1,double Jjx,double Jjz,double hx0, double hy0, double hz0);
        void Values();
        void basis_print();
    private:
        //===========================//                                       |  R
        void outsidehoping( int i);        //| Hamiltonian                    |  O                      
        void insidehoping( int i);         //| Formation                      |  T  
        complex<double> diagonal(int n);   //| Subroutin                      |  O
        void Hspin();                      //| for Rotor                      |  R
        std::vector<int> Lspow;
        //===========================//                                       |
        void output();   
        bool createDirectory(const std::string& path);
        //void QFI(double q);
        void Sx();
        void Sz();
        void QFI(double qx);
        void D();
    public:
        // void total_converge(double U1);
        // void U_phi(double U1);
        void mu_phi();
        //======================================================//
        double Fermi(double e,double m);
        double delta(double x0, double x);
        
        // //=======================================================//
        // void Fermi_dos();
        // void Spin_dos();
        // void DoS();
        // void rotor( int i ,int fm, int fn);
        //========================================================//
        
};

//======================================================//
double input:: Fermi(double e,double m)
{ 
    return 1/(exp((e-m)/T)+1);
}
//=======================================================//
double input::delta(double x0, double x)
{
    double L=0.15;
    double D= (L/(2*M_PI))/(pow(0.01,2)+(x-x0)*(x-x0));
    return D;
}
//=======================================================//
#endif
