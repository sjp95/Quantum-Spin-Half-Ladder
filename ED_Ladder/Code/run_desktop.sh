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

#!/bin/bash
# set -e

# mkdir -p build
# cd build

# cmake ..
# make -j$(nproc)

# ./s1 4 0 1 1 0


#!/bin/bash
# set -e

# mkdir -p build
# # mkdir -p Data

# cmake -S . -B build
# cmake --build build -j$(nproc)

# ./build/s1 4 0 1 1 0


# ./build/r1 4 0 1 1 0


#!/bin/bash
set -e

mkdir -p build
mkdir -p Data

cmake -S . -B build
cmake --build build -j$(nproc)

./build/s1 4 0 1 1 0
 echo "Running read.cpp to read the results from HDF5 file..."
./build/r1 4 1.0 1.0 0.0