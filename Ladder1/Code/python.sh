
# for hz in $(seq 0.0 0.02 0.1) 
# do
#  for Jz in 1.0 #$(seq 1.0 -0.02 0.0)
#  do
#  done
# done
python3 Ed2h.py 100 1 1 & # d2E/dh2 for Jz , Jx Fixed. 

python3 Mh.py 100 1 1 &   # M(h) for Jz , Jx Fixed.