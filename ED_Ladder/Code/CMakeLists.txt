cmake_minimum_required(VERSION 3.16)

project(EigenHDF5 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(HDF5 REQUIRED COMPONENTS C CXX)
find_package(OpenMP REQUIRED)

add_executable(s1 st1.cpp)
add_executable(r1 read.cpp)

target_include_directories(s1 PRIVATE
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/Master
    ${CMAKE_SOURCE_DIR}/Master/Eigen
    ${CMAKE_SOURCE_DIR}/Master/HighFive/include
    ${HDF5_INCLUDE_DIRS}
)

target_include_directories(r1 PRIVATE
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/Master
    ${CMAKE_SOURCE_DIR}/Master/Eigen
    ${CMAKE_SOURCE_DIR}/Master/HighFive/include
    ${HDF5_INCLUDE_DIRS}
)

target_link_libraries(s1 PRIVATE
    HDF5::HDF5
    OpenMP::OpenMP_CXX
    lapack
)

target_link_libraries(r1 PRIVATE
    HDF5::HDF5
)