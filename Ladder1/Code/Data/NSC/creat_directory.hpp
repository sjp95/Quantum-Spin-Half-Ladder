#ifndef CREATDIR_HPP_INCLUDED
#define CREATDIR_HPP_INCLUDED
#include <math.h>
#include <complex>
#include <Eigen/Dense>
#include <vector>
#include <omp.h>
#include <string>
#include "input.hpp"

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/stat.h>
#endif

using namespace std;
using namespace Eigen;
//================================================================================//
//================================================================================//

  bool NSC_input::createDirectory(const std::string& path) 
  {
    #ifdef _WIN32
        // On Windows
        if (CreateDirectory(path.c_str(), NULL) || GetLastError() == ERROR_ALREADY_EXISTS) 
        {
            std::cout << "Directory created successfully." << std::endl;
            return true;
        } 
        else 
        {
            std::cout << "Failed to create directory." << std::endl;
            return false;
        }
    #else
        //On Unix-like systems
        if (mkdir(path.c_str(), 0777) == 0) 
        {
            std::cout << "Directory created successfully.\n" << std::endl;
            return true;
        } 
        else 
        {
            std::cout << "Directory already exist.\n" << std::endl;
            return false;
        }
    #endif
  }


//================================================================================//
//================================================================================//
#endif
