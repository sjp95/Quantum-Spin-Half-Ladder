#!/bin/bash
sub=job.sge
# OMP_NUM_THREADS=3
# export OMP_NUM_THREADS
#source ~/.bashrc
#module load gcc-7.5.0
#module load gcc-11.3.0
#g++ -std=c++17 -I/home/subho/ITensor/ -L/home/subho/ITensor/lib U_O.cpp -litensor -llapack -I /usr/include/lapacke \-L /usr/lib64 -lblas -pthread -o h -fopenmp
#g++ -std=c++17 -I/home/subhajyoti/itensor/ITensor -L/home/subhajyoti/itensor/ITensor/lib U_O.cpp -litensor -llapack -llapacke -lblas -pthread -o h #-fopenmp
/usr/bin/time --verbose ./myappname > main.out
rm main.out

#julia test1.jl 60 -1 -1 1.0
#========================================================================================================================================
#========================================================================================================================================
for hz in 0
do
    for A in 1
    do
    for kpp in {1..60}
        do
        for kpp1 in {30..31}
        do
                #====================================================================
                echo "#PBS  -N  Kiatev_"$kpp"_"$kpp1                > $sub
                echo "#PBS -l nodes=1:ppn=1"                        >> $sub
                echo "#PBS -j oe "                                  >> $sub
                echo "#PBS -o out.log"                              >> $sub
                echo "#PBS -e err.log"                              >> $sub
                echo "cd"    \$PBS_O_WORKDIR                        >> $sub
                echo "date"                                         >> $sub
                echo "julia test2.jl 60 1 1 $A $kpp $kpp1 $hz"      >> $sub
                echo "date"                                         >> $sub
                #====================================================================
                chmod 777 job.sge
                qsub  job.sge
            done
        done
    done
done
#========================================================================================================================================
#========================================================================================================================================
#julia --sysimage /home/subhajyoti/.julia/sysimages/sys_itensors.so test1.jl 40 1 1 $A $kpp $kpp1
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
