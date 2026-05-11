#include <iostream>
#include <string>
#include <Eigen/Dense>
#include <highfive/H5File.hpp>
#include <highfive/eigen.hpp>

using namespace std;
using namespace Eigen;

int main(int argc, char** argv) {
    if (argc != 5) {
        cerr << "Usage: ./r1 N J1 J2 hz\n";
        cerr << "Example: ./r1 4 1.0 1.0 0.0\n";
        return 1;
    }

    int N      = stoi(argv[1]);
    double J1  = stod(argv[2]);
    double J2  = stod(argv[3]);
    double hz  = stod(argv[4]);

    string infile =
        "../Data/results_" +
        to_string(N) + "_" +
        to_string(int(J1 * 100.0)) + "_" +
        to_string(int(J2 * 100.0)) + "_" +
        to_string(int(hz * 100.0)) +
        ".h5";

    try {
        HighFive::File file(infile, HighFive::File::ReadOnly);

        VectorXd eigenvalues;
        MatrixXcd eigenvectors;

        file.getDataSet("eigenvalues").read(eigenvalues);
        file.getDataSet("eigenvectors").read(eigenvectors);

        cout << "Reading file: " << infile << "\n\n";

        cout << "==============================\n";
        cout << "Eigenvalues\n";
        cout << "==============================\n";
        cout << eigenvalues << endl;

        cout << "\n==============================\n";
        cout << "Eigenvector matrix size: "
             << eigenvectors.rows()
             << " x "
             << eigenvectors.cols()
             << endl;
        cout << "==============================\n";

        cout << "\nGround-state eigenvalue:\n";
        cout << eigenvalues(0) << endl;

        cout << "\nGround-state eigenvector:\n";
        cout << eigenvectors.col(0) << endl;
    }
    catch (const std::exception& e) {
        cerr << "HDF5 Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}