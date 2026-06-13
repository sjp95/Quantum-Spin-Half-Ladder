#!/bin/bash
sub=job.sge

#module load gcc-7.5.0
# module load compilers/gcc/9.2.0
g++ -std=c++11 st1.cpp -o h -llapack -I /usr/include/lapacke \-L /usr/lib64
for U in {0..16..1} 
do
#  for V in {50..400..10}
#    do

     #********************************************************************************
     echo "#PBS  -N   Slave_rotor_"$U                               > $sub
     echo "#PBS -l nodes=1:ppn=1"                              >> $sub
     echo "#PBS -j oe "                                        >> $sub
     echo "#PBS -o out.log"                                    >> $sub
     echo "#PBS -e err.log"                                    >> $sub
     echo "cd"    \$PBS_O_WORKDIR                              >> $sub
     echo "date"                                               >> $sub
     echo "./h $U"                                          >> $sub
     echo "date"                                               >> $sub
     #******************************************************************************
     chmod 777 job.sge
     qsub  job.sge

#  done
done


