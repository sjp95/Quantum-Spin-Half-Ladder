#ifndef fftShift_HPP_INCLUDED
#define fftShift_HPP_INCLUDED
#include <iostream>
#include <iomanip>
#include <cmath>
#include <math.h> 
#include <complex>
#include <omp.h>
#include <vector>
#include "input.hpp"
#include <fftw3.h>

using namespace std;
using namespace Eigen;

void NSC_input::fftShift(fftw_complex* data, int size) 
{
    //----------------------------------------------------------------------------------------------------
    //----------------------------------------------------------------------------------------------------
    int half = size / 2;
    fftw_complex* temp = (fftw_complex*) fftw_malloc(half * sizeof(fftw_complex)); // Allocate temporary array
    //----------------------------------------------------------------------------------------------------
    //----------------------------------------------------------------------------------------------------
    // Copy the first half of the array to temporary array
    for (int i = 0; i < half; ++i) {
        temp[i][0] = data[i][0];
        temp[i][1] = data[i][1];
    }
    //----------------------------------------------------------------------------------------------------
    //----------------------------------------------------------------------------------------------------
    // Shift the second half of the array to the beginning
    //----------------------------------------------------------------------------------------------------
    //----------------------------------------------------------------------------------------------------
    for (int i = 0; i < half; ++i) {
        data[i][0] = data[i + half][0];
        data[i][1] = data[i + half][1];
    }
    //----------------------------------------------------------------------------------------------------
    //----------------------------------------------------------------------------------------------------

    // Copy the temporary array to the second half of the array
    for (int i = 0; i < half; ++i) {
        data[i + half][0] = temp[i][0];
        data[i + half][1] = temp[i][1];
    }
    //----------------------------------------------------------------------------------------------------
    //----------------------------------------------------------------------------------------------------
    fftw_free(temp); // Free temporary array
}
#endif












    