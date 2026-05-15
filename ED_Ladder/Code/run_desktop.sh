#!/bin/bash
#sub=job.sge

#module load gcc-7.5.0
# module load compilers/gcc/9.2.0
#g++ -std=c++20 st1.cpp -o h -llapack -fopenmp #-I /usr/include/lapacke \-L /usr/lib64
#./h 4 0 1 1 0

# for U in {0..160..10} 
# do

#      #********************************************************************************
#      echo "#PBS  -N   Slave_rotor_"$U                               > $sub
#      echo "#PBS -l nodes=1:ppn=1"                              >> $sub
#      echo "#PBS -j oe "                                        >> $sub
#      echo "#PBS -o out.log"                                    >> $sub
#      echo "#PBS -e err.log"                                    >> $sub
#      echo "cd"    \$PBS_O_WORKDIR                              >> $sub
#      echo "date"                                               >> $sub
#      echo "./h $U"                                          >> $sub
#      echo "date"                                               >> $sub
#      #******************************************************************************
#      chmod 777 job.sge
#      qsub  job.sge

# done


#=============================================================================#
# This script compiles and runs the desktop version of the program Without MKL
#=============================================================================#
#!/bin/bash
# set -e

# mkdir -p build
# #mkdir -p Data

# cmake -S . -B build
# cmake --build build -j$(nproc)

# ./build/s1 4 0 1 1 0
# echo "Running read.cpp to read the results from HDF5 file..."
#./build/r1 4 1.0 1.0 0.0
#=============================================================================#
# This script compiles and runs the desktop version of the program With MKL
#=============================================================================#

!/bin/bash
set -e

# Initialize oneAPI environment for runtime libraries
if [ -f "/opt/intel/oneapi/setvars.sh" ]; then
    source /opt/intel/oneapi/setvars.sh --force
fi

# Performance tuning: Use all physical cores
export MKL_NUM_THREADS=$(nproc)
export OMP_NUM_THREADS=2 #$(nproc)

# Force Eigen to use MKL backend (if s3.cpp includes Eigen)
export EIGEN_USE_MKL_ALL=1

mkdir -p build

cmake -S . -B build
cmake --build build -j$(nproc)

echo "Starting execution with $MKL_NUM_THREADS threads..."
   
for hz in {0..150..2} #$(seq 1.02 0.02 1.50) 
do
 for Jz in 100.0 #$(seq 1.0 -0.02 0.0)
 do
  ./build/s1 12 0.0 100.0 $Jz $hz pbc
 done
done

# for i in $(seq 112 2 116)
# do
#     printf -v hz "%d.%02d" $((i/100)) $((i%100))
#     for Jz in 1.0
#     do
#         ./build/s1 12 0 1.0 "$Jz" "$hz"
#     done
# done
#-----------------------------------------------------------------------------#

 for Jz in 1.0 #$(seq 1.0 -0.02 0.0)
 do
  python3 Ed2h.py 12 1.0 $Jz
  python3 Mz.py 12 1.0 $Jz
  cd ..
  python3 plotEd2h.py 12 1.0 $Jz
  python3 Mh.py 12 1.0 $Jz
  cd Code
 done

# python3 Ed2h.py 4 1.0 1.0
# cd ..
#python3 plotEd2h.py 4 1.0 1.0

#=============================================================================#
# Alternative
#=============================================================================#
#!/bin/bash
# set -e

# if [ -f "/opt/intel/oneapi/setvars.sh" ]; then
#     source /opt/intel/oneapi/setvars.sh --force
# fi

# export OMP_NUM_THREADS=$(nproc)
# export MKL_NUM_THREADS=1
# export MKL_DYNAMIC=FALSE

# mkdir -p build
# #mkdir -p Data

# cmake -S . -B build
# cmake --build build -j$(nproc)

# echo "Running with OMP=$OMP_NUM_THREADS MKL=$MKL_NUM_THREADS"

# ./build/s1 4 0 1 1 0
#=============================================================================#
#=============================================================================#
