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

./h 12 5.0 0.18

# for T in  0.1 50 100 200  
# do

#      #********************************************************************************
#      echo "#PBS  -N   Slave_rotor_"$T                          > $sub
#      echo "#PBS -l nodes=1:ppn=32"                             >> $sub
#      echo "#PBS -j oe "                                        >> $sub
#      echo "#PBS -o out.log"                                    >> $sub
#      echo "#PBS -e err.log"                                    >> $sub
#      echo "module load compilers/parallel_studio_xe_2018_update3/compiler/default"     >> $sub
#      echo "module load compilers/parallel_studio_xe_2018_update3/mkl/default"     >> $sub
#      echo "cd"    \$PBS_O_WORKDIR                               >> $sub
#      echo "date"                                               >> $sub
#      echo "./h 12 $T"                                          >> $sub
#      echo "date"                                               >> $sub
#      #******************************************************************************
#      chmod 777 job.sge
#      qsub  job.sge

# done
