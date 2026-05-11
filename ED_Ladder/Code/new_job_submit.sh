sub=job.sge
module load compilers/parallel_studio_xe_2018_update3/mkl/default
module load compilers/parallel_studio_xe_2018_update3/parallel_studio_xe_2018/default
module load openmpi-4.1.4
module load gcc-7.5.0

export MKL_NUM_THREADS=10
export OMP_NUM_THREADS=10
g++ -std=c++17 -O3 st1.cpp -o h\
  -I${MKLROOT}/include \
  -L${MKLROOT}/lib/intel64 \
  -Wl,--start-group \
    -lmkl_intel_lp64 -lmkl_core -lmkl_intel_thread \
  -Wl,--end-group \
  -liomp5 -lpthread -lm -ldl -fopenmp

module load compilers/parallel_studio_xe_2018_update3/compiler/default
module load compilers/parallel_studio_xe_2018_update3/mkl/default

#./h 12 0.1

for T in  0.001 0.1 0.2 0.3 0.4 0.5 0.6 0.8 1.0 1.5 2.0
do

     #********************************************************************************
     echo "#PBS  -N   Slave_rotor_"$T                          > $sub
     echo "#PBS -l nodes=1:ppn=32"                             >> $sub
     echo "#PBS -j oe "                                        >> $sub
     echo "#PBS -o out.log"                                    >> $sub
     echo "#PBS -e err.log"                                    >> $sub
     echo "module load compilers/parallel_studio_xe_2018_update3/compiler/default"     >> $sub
     echo "module load compilers/parallel_studio_xe_2018_update3/mkl/default"     >> $sub
     echo "cd"    \$PBS_O_WORKDIR                               >> $sub
     echo "date"                                               >> $sub
     echo "./h 12 $T 1.0"                                          >> $sub
     echo "date"                                               >> $sub
     #******************************************************************************
     chmod 777 job.sge
     qsub  job.sge

done












# ... (your existing module loads) ...

# Compile once before the loop
mkdir -p build && cd build
cmake .. && make -j4
cd ..

for T in 0.001 0.1 0.2 0.3 0.4 0.5 0.6 0.8 1.0 1.5 2.0
do
     echo "#PBS -N Slave_rotor_$T" > $sub
     echo "#PBS -l nodes=1:ppn=32" >> $sub
     # ... (other PBS headers) ...
     
     echo "module load compilers/parallel_studio_xe_2018_update3/mkl/default" >> $sub
     # IMPORTANT: Load HDF5 runtime in the job too
     echo "module load hdf5" >> $sub 
     
     echo "cd \$PBS_O_WORKDIR" >> $sub
     # Point to the executable in the build folder
     echo "./build/h 12 $T 1.0" >> $sub
     
     chmod 777 job.sge
     qsub job.sge
done

