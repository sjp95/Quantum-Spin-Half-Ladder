#!/bin/bash
# sub=job.sge
# # OMP_NUM_THREADS=3
# # export OMP_NUM_THREADS
# #source ~/.bashrc
# #module load gcc-7.5.0
# module load gcc-11.3.0
# g++ -std=c++17 -I/home/subho/ITensor/ -L/home/subho/ITensor/lib U_O.cpp -litensor -llapack -I /usr/include/lapacke \-L /usr/lib64 -lblas -pthread -o h -fopenmp
# #g++ -std=c++17 -I/home/subhajyoti/itensor/ITensor -L/home/subhajyoti/itensor/ITensor/lib U_O.cpp -litensor -llapack -llapacke -lblas -pthread -o h #-fopenmp
# /usr/bin/time --verbose ./myappname > main.out
# rm main.out
export JULIA_NUM_THREADS=4
# #========================================================================================================================================
# #========================================================================================================================================
# for A in 1
# do
#    for kpp in 18
#     do
#        for kpp1 in 3
#        do
#             #====================================================================
#             echo "#PBS  -N  RIXS_t-J"$kpp"_"$kpp1                > $sub
#             echo "#PBS -l nodes=1:ppn=1"                        >> $sub
#             echo "#PBS -j oe "                                  >> $sub
#             echo "#PBS -o out.log"                              >> $sub
#             echo "#PBS -e err.log"                              >> $sub
#             echo "cd"    \$PBS_O_WORKDIR                        >> $sub
#             echo "date"                                         >> $sub
#             echo "./h $kpp $kpp1 36 18 18 $A"                   >> $sub
#             echo "date"                                         >> $sub
#             #====================================================================
#             chmod 777 job.sge
#             qsub  job.sge
#         done
#     done
# done
#========================================================================================================================================
#========================================================================================================================================

#julia --sysimage /home/subhajyoti/.julia/sysimages/sys_itensors.so test1.jl 30 1 1 0 2 2
julia --sysimage /home/subhajyoti/.julia/sysimages/sys_itensors.so test1.jl 60 1 1 0.5 #2 2
julia --sysimage /home/subhajyoti/.julia/sysimages/sys_itensors.so test2.jl 60 1 1 0 2 2 0.5

#julia --sysimage /home/subhajyoti/.julia/sysimages/sys_itensors.so test_test2.jl 60 1 1 0 5

#./data.sh
# for A in 1
# do
#    for kpp in 15
#     do
#        for kpp1 in {4..27}
#        do
#          ./h $kpp $kpp1 30 15 15 $A
#         done
#     done
# done

for hz in $(seq 0.52 0.02 0.7) 
do
 for Jz in 1.0 #$(seq 1.0 -0.02 0.0)
 do
  julia test1.jl 100 1.0 $Jz $hz &
 done
done