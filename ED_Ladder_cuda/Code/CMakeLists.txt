#=============================================================================#
# This script compiles and runs the desktop version of the program Without MKL
#=============================================================================#
# cmake_minimum_required(VERSION 3.16)

# project(EigenHDF5 LANGUAGES C CXX)

# set(CMAKE_CXX_STANDARD 20)
# set(CMAKE_CXX_STANDARD_REQUIRED ON)

# find_package(HDF5 REQUIRED COMPONENTS C CXX)
# find_package(OpenMP REQUIRED)

# add_executable(s1 st1.cpp)
# add_executable(r1 read.cpp)

# target_include_directories(s1 PRIVATE
#     ${CMAKE_SOURCE_DIR}
#     ${CMAKE_SOURCE_DIR}/Master
#     ${CMAKE_SOURCE_DIR}/Master/Eigen
#     ${CMAKE_SOURCE_DIR}/Master/HighFive/include
#     ${HDF5_INCLUDE_DIRS}
# )

# target_include_directories(r1 PRIVATE
#     ${CMAKE_SOURCE_DIR}
#     ${CMAKE_SOURCE_DIR}/Master
#     ${CMAKE_SOURCE_DIR}/Master/Eigen
#     ${CMAKE_SOURCE_DIR}/Master/HighFive/include
#     ${HDF5_INCLUDE_DIRS}
# )

# target_link_libraries(s1 PRIVATE
#     HDF5::HDF5
#     OpenMP::OpenMP_CXX
#     lapack
# )

# target_link_libraries(r1 PRIVATE
#     HDF5::HDF5
# )


#=============================================================================#
# This script compiles and runs the desktop version of the program With MKL
#=============================================================================#

cmake_minimum_required(VERSION 3.16)
project(EigenHDF5 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- MKL Configuration ---
set(MKLROOT "/opt/intel/oneapi/mkl/2026.0")
set(INTEL_LIB_PATH "/opt/intel/oneapi/compiler/latest/lib")

find_package(HDF5 REQUIRED COMPONENTS C CXX)
find_package(OpenMP REQUIRED)

add_executable(s1 st1.cpp)
add_executable(r1 read.cpp)

# Common include directories
set(COMMON_INCLUDES
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/Master
    ${CMAKE_SOURCE_DIR}/Master/Eigen
    ${CMAKE_SOURCE_DIR}/Master/HighFive/include
    ${HDF5_INCLUDE_DIRS}
    ${MKLROOT}/include
)

target_include_directories(s1 PRIVATE ${COMMON_INCLUDES})
target_include_directories(r1 PRIVATE ${COMMON_INCLUDES})

# Link s1 with MKL and OpenMP
target_link_libraries(s1 PRIVATE
    HDF5::HDF5
    OpenMP::OpenMP_CXX
    -L${MKLROOT}/lib
    -L${INTEL_LIB_PATH}
    -Wl,--start-group
      ${MKLROOT}/lib/libmkl_intel_lp64.a
      ${MKLROOT}/lib/libmkl_core.a
      ${MKLROOT}/lib/libmkl_intel_thread.a
    -Wl,--end-group
    iomp5
    pthread
    m
    dl
)

target_link_libraries(r1 PRIVATE
    HDF5::HDF5
)
#=============================================================================#
# Alternative
#=============================================================================#
# cmake_minimum_required(VERSION 3.16)

# project(EigenHDF5 LANGUAGES C CXX)

# set(CMAKE_CXX_STANDARD 20)
# set(CMAKE_CXX_STANDARD_REQUIRED ON)

# find_package(HDF5 REQUIRED COMPONENTS C CXX)
# find_package(OpenMP REQUIRED)

# if(NOT DEFINED ENV{MKLROOT})
#     message(FATAL_ERROR "MKLROOT not set. Run: source /opt/intel/oneapi/setvars.sh")
# endif()

# set(MKLROOT $ENV{MKLROOT})

# add_executable(s1 st1.cpp)
# add_executable(r1 read.cpp)

# target_compile_definitions(s1 PRIVATE EIGEN_USE_MKL_ALL)

# set(COMMON_INCLUDES
#     ${CMAKE_SOURCE_DIR}
#     ${CMAKE_SOURCE_DIR}/Master
#     ${CMAKE_SOURCE_DIR}/Master/Eigen
#     ${CMAKE_SOURCE_DIR}/Master/HighFive/include
#     ${HDF5_INCLUDE_DIRS}
#     ${MKLROOT}/include
# )

# target_include_directories(s1 PRIVATE ${COMMON_INCLUDES})

# target_include_directories(r1 PRIVATE
#     ${CMAKE_SOURCE_DIR}
#     ${CMAKE_SOURCE_DIR}/Master
#     ${CMAKE_SOURCE_DIR}/Master/Eigen
#     ${CMAKE_SOURCE_DIR}/Master/HighFive/include
#     ${HDF5_INCLUDE_DIRS}
# )

# target_link_libraries(s1 PRIVATE
#     HDF5::HDF5
#     OpenMP::OpenMP_CXX
#     -Wl,--start-group
#       ${MKLROOT}/lib/intel64/libmkl_intel_lp64.a
#       ${MKLROOT}/lib/intel64/libmkl_core.a
#       ${MKLROOT}/lib/intel64/libmkl_intel_thread.a
#     -Wl,--end-group
#     iomp5
#     pthread
#     m
#     dl
# )

# target_link_libraries(r1 PRIVATE
#     HDF5::HDF5
# )