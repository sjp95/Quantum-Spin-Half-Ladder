// #ifndef CREATDIR_HPP_INCLUDED
// #define CREATDIR_HPP_INCLUDED
// #include <math.h>
// #include <complex>
// #include <Eigen/Dense>
// #include <vector>
// #include <omp.h>
// #include <string>
// #include "input.hpp"

// #ifdef _WIN32
// #include <windows.h>
// #else
// #include <sys/stat.h>
// #endif

// using namespace std;
// using namespace Eigen;
// //================================================================================//
// //================================================================================//

//   bool input::createDirectory(const std::string& path)     
//   {
//     #ifdef _WIN32
//         // On Windows
//         if (CreateDirectory(path.c_str(), NULL) || GetLastError() == ERROR_ALREADY_EXISTS) 
//         {
//             std::cout << "Directory created successfully." << std::endl;
//             return true;
//         } 
//         else 
//         {
//             std::cout << "Failed to create directory." << std::endl;
//             return false;
//         }
//     #else
//         //On Unix-like systems
//         if (mkdir(path.c_str(), 0777) == 0) 
//         {
//             std::cout << "Directory created successfully.\n" << std::endl;
//             return true;
//         } 
//         else 
//         {
//             std::cout << "Directory already exist.\n" << std::endl;
//             return false;
//         }
//     #endif
//   }


// //================================================================================//
// //================================================================================//
// #endif

//===================================================================================//
//===================================================================================//

#ifndef CREATDIR_HPP_INCLUDED
#define CREATDIR_HPP_INCLUDED

#include <iostream>
#include <string>
#include <filesystem>
#include "input.hpp"

using namespace std;
namespace fs = std::filesystem;

//================================================================================//
// Recursive directory creation (mkdir -p equivalent) Latest update with c++20
//================================================================================//

bool input::createDirectory(const std::string& path)
{
    try
    {
        if (fs::exists(path))
        {
            cout << "Directory already exists: " << path << endl;
            return true;
        }

        if (fs::create_directories(path))
        {
            cout << "Directory created successfully: " << path << endl;
            return true;
        }

        cout << "Failed to create directory: " << path << endl;
        return false;
    }
    catch (const fs::filesystem_error& e)
    {
        cerr << "Filesystem Error: " << e.what() << endl;
        return false;
    }
}

//================================================================================//

#endif
//===================================================================================//
//===================================================================================//
