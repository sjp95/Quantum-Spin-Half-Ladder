#ifndef SLAVE_ROTOR_HPP_INCLUDED
#define SLAVE_ROTOR_HPP_INCLUDED
#include <math.h>
#include <complex>
#include "input.hpp"
#include "matworks.hpp"
#include "Operators/Hspin.hpp"
#include <Eigen/Dense>
#include <highfive/H5File.hpp>
#include <highfive/eigen.hpp>
#include "creat_directory.hpp"
#include "Operators/sx.hpp"
#include "Operators/sz.hpp"
//#include "Operators/QFI.hpp"
// #include "Rotor/spinconverge.hpp"
// #include "Rotor/oioj.hpp"

//#include "Dos/dos.hpp"
#include "values.hpp"
using namespace std;
using namespace Eigen;
char title3[100];
char title4[100];
char title5[100];

void input::besis(int NN1,double Jjx,double Jjz,double hx0, double hy0, double hz0)
{
    N=NN1;
    J1=Jjx;
    J2=Jjz;
    hx= hx0;
    hy= hy0;
    hz= hz0;

    Ls=2*lz+1;
    ls = 0;                 // Besis count start
    le = pow(Ls,N);         // Besis count End
    //==============================//
    H= MatrixXcd :: Zero(le,le);
    Jx= MatrixXcd :: Zero(N,N);
    Jz= MatrixXcd :: Zero(N,N); 
    //t= MatrixXcd::Zero(N,N);
    evs = MatrixXcd :: Zero(le,le);
    es = VectorXd :: Zero(le);
    //==============================//
    cout<< "==============================="<<endl;
    cout<< "Data Alocation Done"<<endl;
    cout<< "==============================="<<endl;
    Values();
}



//==========================================================================================//
void input::output()
{
//     cout<<"\nU: "<<U<<"\nPhi: "<< O.transpose()<<"\nRotor occupation: "<< Stotal<<endl;
}

//==========================================================================================//    
void input::basis_print()
{
    cout<< "==============================="<<endl;
    cout<< "Basis Generated"<<endl;
    cout<< "==============================="<<endl;
    for (int i=0; i<le; i++)
    {
        int n=i;
        VectorXi nnt = VectorXi :: Zero(N);
        for ( int j =0; j<N; j++)
        {
            double reminder = n%Ls;
            n=n/Ls;
            nnt(j)=int(reminder);
        }
        cout<< i <<"  |"<< nnt.transpose()<<">"<<endl;
        
    }
    cout<< "==============================="<<endl;
}
//==========================================================================================//    

void input::mu_phi()
{
    bool tut = createDirectory("../Data/Eigen/Eigen");

    std::string outfile =
        "../Data/Eigen/Eigen/EigenSpectrum_" +
        std::to_string(N) + "_" +
        std::to_string(int(J1 * 100.0)) + "_" +
        std::to_string(int(J2 * 100.0)) + "_" +
        std::to_string(int(hz * 100.0)) + ".h5";

    bool loaded_from_file = false;

    //==========================================================
    // Try loading existing eigenspectrum
    //==========================================================
    if (std::filesystem::exists(outfile))
    {
        try
        {
            cout << "===============================\n";
            cout << "Existing HDF5 file found.\n";
            cout << "Loading eigenspectrum...\n";
            cout << "===============================\n";

            HighFive::File file(outfile, HighFive::File::ReadOnly);

            file.getDataSet("eigenvalues").read(es);
            file.getDataSet("eigenvectors").read(evs);

            // Free Hamiltonian memory
            MatrixXcd().swap(H);

            loaded_from_file = true;

            cout << "HDF5 read successful\n";
        }
        catch (const std::exception& e)
        {
            cerr << "HDF5 Read Error: " << e.what() << endl;
            cerr << "Recomputing eigenspectrum...\n";
        }
    }

    //==========================================================
    // Compute if file absent or read failed
    //==========================================================
    if (!loaded_from_file)
    {
        Hspin();

        cout << "===============================\n";
        cout << "H generated\n";
        cout << "H(0,0): " << H(0,0) << endl;
        cout << "===============================\n";

        basis_print();

        cout << "===============================\n";
        cout << "Diagonalizing Hamiltonian...\n";
        cout << "===============================\n";

        pair<MatrixXcd, VectorXd> e = Eigenspectrum(H);

        es = e.second;
        evs = e.first;

        try
        {
            HighFive::File file(outfile, HighFive::File::Overwrite);

            file.createDataSet("eigenvalues", es);
            file.createDataSet("eigenvectors", evs);

            cout << "HDF5 write successful\n";
        }
        catch (const std::exception& e)
        {
            cerr << "HDF5 Write Error: " << e.what() << endl;
        }

        // Free Hamiltonian after diagonalization
        MatrixXcd().swap(H);
    }

    //==========================================================
    // Observables
    //==========================================================
    Sx();
    Sz();
}
//=======================================================//
#endif
