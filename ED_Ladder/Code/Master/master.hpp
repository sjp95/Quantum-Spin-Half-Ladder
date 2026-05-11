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

void input:: mu_phi()
{
    
    Hspin();  
    pair<MatrixXcd, VectorXd> e = Eigenspectrum(H);
    es=e.second;
    evs=e.first;
    //basis_print();
    

    // HighFive::File file("results.h5", HighFive::File::Overwrite);
    // file.createDataSet("eigenvalues", es);
    // file.createDataSet("eigenvectors", evs);

    bool tut=createDirectory("../Data");
    std::string outfile ="../Data/results_" + std::to_string(N) + "_" +    std::to_string(int(J1*100.0)) + "_" +    std::to_string(int(J2*100.0)) + "_" +    std::to_string(int(hz*100.0)) +  ".h5";

    try {
        HighFive::File file(outfile, HighFive::File::Overwrite);

        file.createDataSet("eigenvalues", es);
        file.createDataSet("eigenvectors", evs);
        cout << "HDF5 write successful\n";
    }
    catch (const std::exception& e) {
        cerr << "HDF5 Error: " << e.what() << endl;
    }

    
    //QFI(M_PI);
    
    //cout<< es <<"\n"<<endl;
    //cout<< evs.col(0) <<endl;
    
}
//=======================================================//
#endif
