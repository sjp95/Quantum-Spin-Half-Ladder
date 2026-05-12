#ifndef MATWORKS_HPP_INCLUDED
#define MATWORKS_HPP_INCLUDED

#include <iostream>
#include <cmath>
#define EIGEN_USE_MKL_ALL
#include <Eigen/Dense>

#include <vector>
#include <complex>

//#define EIGEN_USE_MKL_ALL
// #include <Accelerate/Accelerate.h>
// #include <lapacke.h>
// #include <essl.h>
using namespace std;
using namespace Eigen;


typedef std::complex<double> cd;
typedef std::pair<Eigen::MatrixXcd, Eigen::VectorXd> Spectrum;
typedef std::pair<Eigen::MatrixXcd, std::vector<double> > stdSpectrum;

using Eigen::MatrixXcd;
using Eigen::VectorXd;
using std::cout;
using std::endl;
using std::pair;
using std::vector;

extern int L;
int L;

double filter_d(double x) { return (abs(x) <= 1e-4) ? 0 : x; }
void increment_test(const int &x, int &y) { y = x + y; }

extern "C" {
void zheev_( char* jobz, char* uplo, int* n, __complex__ double * a, int* lda, double* w, __complex__ double * work, int* lwork, double* rwork, int* info );
void zgeev_(char* jobz, char* uplo, int* n, __complex__ double * a, int* lda , __complex__ double * w, __complex__ double * vl, int* LDVL, __complex__ double *vr, int* LDVR,__complex__ double * WORK, int* lwork, double* rwork, int* info);	
}


bool zheev_cpp(MatrixXcd &A, vector<double> &lambda, char eigenvec_choice = 'N')
{
    int N = A.cols();
    int LDA = A.outerStride();
    int INFO = 0;
    double *w = new double[N];
    char Nchar = 'N';
    char Vchar = 'V';
    char Uchar = 'U';
    int LWORK = int(A.size()) * 4;
    __complex__ double *WORK = new __complex__ double[LWORK];
    double *RWORK = new double[3 * LDA];

    zheev_(&eigenvec_choice, &Uchar, &N, reinterpret_cast<__complex__ double *>(A.data()), &LDA, w, WORK, &LWORK, RWORK, &INFO);

    lambda.clear();
    for (int i = 0; i < N; i++)
        lambda.push_back(w[i]);

    delete[] w;
    delete[] RWORK;
    delete[] WORK;
    return INFO == 0;
}

bool zgeev_cpp(MatrixXcd &A, vector<double> &lambda, char eigenvec_choice = 'N')
{
    int N = A.cols();
    int LDA = A.outerStride();
    int INFO = 0;
    __complex__ double *w = new __complex__ double[N];
    __complex__ double *vl;
    __complex__ double *vr;
    char Nchar = 'N';
    char Vchar = 'V';
    char Uchar = 'U';
    int LWORK = pow(2, N);
    __complex__ double *WORK = new __complex__ double[LWORK];
    double *RWORK = new double[LWORK];

    zgeev_(&Nchar, &eigenvec_choice, &N, reinterpret_cast<__complex__ double *>(A.data()), &LDA, w, vl, &LDA, vr, &LDA, WORK, &LWORK, RWORK, &INFO);

    lambda.clear();
    for (int i = 0; i < N; i++)
        lambda.push_back(__real__ w[i]);

    delete[] w;
    delete[] RWORK;
    delete[] WORK;
    return INFO == 0;
}

vector<double> stdEigenvalues(MatrixXcd &A, bool (*diagonalization_routine)(MatrixXcd &, vector<double> &, char) = &zheev_cpp)
{
    std::vector<double> lambda;
    if (diagonalization_routine(A, lambda, 'N'))
    {
        return lambda;
    }
    else
    {
        std::cout<< "Sorry \n Could not compute the eigenvalues"<< endl;
        return {0,0};
    }
}

VectorXd Eigenvalues(MatrixXcd &A, bool (*diagonalization_routine)(MatrixXcd &, vector<double> &, char) = &zheev_cpp)
{
    std::vector<double> lambda;
    if (diagonalization_routine(A, lambda, 'N'))
    {
        Eigen::Map<Eigen::ArrayXd> b(lambda.data(), lambda.size());
        return b;
    }
    else
    {
        std::cout<< "Sorry \n Could not compute the eigenvalues"<< endl;
        return {0,0};
    }
}

MatrixXcd Eigenvectors(MatrixXcd &A, bool (*diagonalization_routine)(MatrixXcd &, vector<double> &, char) = &zheev_cpp)
{
    std::vector<double> lambda;
    if (diagonalization_routine(A, lambda, 'V'))
    {
        return A;
    }
    else
    {
        std::cout<< "Sorry \n Could not compute the eigenvectors"<< endl;
        return A;
    }
}

pair<MatrixXcd, vector<double> > stdEigenspectrum(MatrixXcd &A, bool (*diagonalization_routine)(MatrixXcd &, vector<double> &, char) = &zheev_cpp)
{
    std::vector<double> lambda;
    if (diagonalization_routine(A, lambda, 'V'))
    {
        return make_pair(A, lambda);
    }
    else
    {
        std::cout<< "Sorry \n Could not compute the eigenvalues & eigenvectors"<< endl;
        return make_pair(A, lambda);
    }
}

pair<MatrixXcd, VectorXd> Eigenspectrum(MatrixXcd &A, bool (*diagonalization_routine)(MatrixXcd &, vector<double> &, char) = &zheev_cpp)
{
    std::vector<double> lambda;
    if (diagonalization_routine(A, lambda, 'V'))
    {
        Eigen::Map<Eigen::ArrayXd> b(lambda.data(), lambda.size());
        return make_pair(A, b);
    }
    else
    {
        std::cout<< "Sorry \n Could not compute the eigenvalues & eigenvectors"<< endl;
        Eigen::Map<Eigen::ArrayXd> b(lambda.data(), lambda.size());
        return make_pair(A,b);
    }
}

#endif
