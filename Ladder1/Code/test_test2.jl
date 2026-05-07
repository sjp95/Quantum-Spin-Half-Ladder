include("input.jl")
using Base.Filesystem
using ITensors, ITensorMPS
using Base.Threads

let

  #===========================================================================#
             #================= Parameters ===================#
  #===========================================================================#
  Kitayev.N = parse(Int64, ARGS[1])
  Kitayev.Jx = parse(Float64, ARGS[2])
  Kitayev.Jy = parse(Float64, ARGS[3])
  order = parse(Int64, ARGS[4])
  Kitayev.hz = parse(Float64, ARGS[5])
  Kitayev.longrange = 1
  Kitayev.sites = siteinds("S=1/2",N;conserve_qns=false)
  #===========================================================================#
  #===========================================================================#

  #===========================================================================#
        #================= Printing of Parameters ===================#
  #===========================================================================#
  
  Kitayev.Values()
  Kitayev.printMatrix(Kitayev.JJx)
  Kitayev.printMatrix(Kitayev.JJy)

  #===========================================================================#
  H = Kitayev.Hamiltonian()  # Hamiltonian

  #===========================================================================#
     #================= DMRG to claculate Groundstate ===================#
  #===========================================================================#
  psi0 = random_mps(Kitayev.sites; linkdims=100)
  @show flux(psi0)
  nsweeps = 20
  noise = [1e-3, 1e-6, 1e-8, 1e-10, 1e-12]
  maxdim = [10, 20, 100, 500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
  cutoff = [1E-14]
  energy, psi = dmrg(H, psi0; nsweeps, maxdim, cutoff,)
  println("\n Groundstate Energy: $energy \n")
  #===========================================================================#
  #===========================================================================#

   #===========================================================================#
  #===========================================================================#
  file_name = "New"
  Kitayev.Make_Directory("../Data")
  Kitayev.Make_Directory("../Data/NSC")
  Kitayev.Make_Directory("../Data/NSC/Test/")
  if order == 0
    directory_path = "../Data/NSC/Test/SZ"
    Kitayev.Make_Directory(directory_path)
  elseif order == 1
    directory_path = "../Data/NSC/Test/SZiSZj"
    Kitayev.Make_Directory(directory_path)
  end
  #===========================================================================#
  #===========================================================================#

  #println("$ii \t $jj")
  psi00 = psi
  psi01 = psi
  psi1 =psi#apply(O1,psi;cutoff=1e-12,maxdim=1000) # O_ii|g⟩= |ii⟩
  psi2 =psi#apply(O2,psi00;cutoff=1e-12,maxdim=1000) # O_jj|g⟩= |jj⟩
  print(inner(psi2,psi1), "\n")

  #===========================================================================#
  #===========================================================================#
  Jx = Int(Kitayev.Jx * 100)
  Jy = Int(Kitayev.Jy * 100)
  if order == 0
    file_name = "../Data/NSC/Test/SZ/SZ_$(Kitayev.N)_$(Jx)_$(Jy).dat"
  elseif order == 1
    file_name = "../Data/NSC/Test/SZiSZj/SZiSZj_$(Kitayev.N)_$(Jx)_$(Jy).dat"
  end
  #===========================================================================#
  #===========================================================================#
  file = open(file_name, "w")
  println(file, "#ttotal <Sz(SL,ttotal).Sz(SR,0)> t(ms) SR   SL")
  #===========================================================================#
           #================= Time Evolution ===================#
  #===========================================================================#

  #===========================================================================#
  #===========================================================================#
    cutofft = 1E-8
    tau = 0.02
    ttotal = 10.0
    gates=Kitayev.TEBD_gates(tau)

    for t in 0.0:tau*5:ttotal
      x = psi1 # O_ii|g⟩= |ii⟩
      y = psi2 # O_jj|g⟩= |jj⟩
      prefactor = exp(im * 0 * energy) # exp(+iE_gt)
      Sz = inner(x',H,x)
      Sz = Sz * prefactor # exp(+iE_gt)x⟨g| O_ii exp(-iHt) O_jj |g⟩
      SZreal = real(Sz-energy)
      SZimag = imag(Sz)
      println(file, "$t \t $SZreal \t $SZimag")
      println("$t \t $SZreal \t $SZimag")
      t ≈ ttotal && break
      for i in 1:1:5 
        psi1 = apply(gates, psi1; cutoff=1e-12, maxdim=1000) # Gate Evolution exp(-iHt)|jj⟩
      end
     
    end
#===========================================================================#
#===========================================================================#

 

  return
end



  


#   # O1=Kitayev.Operators(order,ii)
#   # O2=Kitayev.Operators(order,jj)

#   println("$ii \t $jj")
#   psi00 = psi
#   psi01 = psi
#   psi1 =psi#apply(O1,psi;cutoff=1e-12,maxdim=1000) # O_ii|g⟩= |ii⟩
#   psi2 =psi#apply(O2,psi00;cutoff=1e-12,maxdim=1000) # O_jj|g⟩= |jj⟩
#   print(inner(psi2,psi1), "\n")

#   #===========================================================================#
#   #===========================================================================#
#   Jx = Int(Kitayev.Jx * 100)
#   Jy = Int(Kitayev.Jy * 100)
#   if order == 0
#     file_name = "../Data/NSC/Test/SZ/SZ_$(Kitayev.N)_$(Jx)_$(Jy).dat"
#   elseif order == 1
#     file_name = "../Data/NSC/Test/SZiSZj/SZiSZj_$(Kitayev.N)_$(Jx)_$(Jy).dat"
#   end
#   #===========================================================================#
#   #===========================================================================#
#   file = open(file_name, "w")
#   println(file, "#ttotal <Sz(SL,ttotal).Sz(SR,0)> t(ms) SR   SL")
#   #===========================================================================#
#            #================= Time Evolution ===================#
#   #===========================================================================#
#   #===========================================================================#
#     #===========================================================================#

#     cutofft = 1E-8
#     tau = 0.2
#     ttotal = 30.0
#     gates=Kitayev.TEBD_gates(tau)

#     for t in 0.0:tau:ttotal
#       x = psi1 # O_ii|g⟩= |ii⟩
#       y = psi2 # O_jj|g⟩= |jj⟩
#       prefactor = exp(im * 0 * energy) # exp(+iE_gt)
#       Sz = inner(x',H,x)
#       Sz = Sz * prefactor # exp(+iE_gt)x⟨g| O_ii exp(-iHt) O_jj |g⟩
#       SZreal = real(Sz)
#       SZimag = imag(Sz)
#       println(file, "$t \t $SZreal \t $SZimag  \t $ii \t $jj ")
#       #println("$t \t $SZreal \t $SZimag")
#       t ≈ ttotal && break
#       psi1 = apply(gates, psi1; cutoff=1e-12, maxdim=1000) # Gate Evolution exp(-iHt)|jj⟩
#     end
# #===========================================================================#
# #===========================================================================#
#   return
# end



#===========================================================================#
#Testing
#===========================================================================#


# for t in 0.0:tau:ttotal
    
#   #---------------------------------------------------------------------------#
#   psi00=psi1
#   x=psi1 # O_ii|g⟩= |ii⟩
#   y=apply(H,psi00;cutoff=1e-12,maxdim=1000)#psi2 # O_jj|g⟩= |jj⟩
#   prefactor = 1#exp(im * 0* energy) # exp(+iE_gt)
#   Sz=inner(y,x) 
#   Sz=Sz*prefactor # exp(+iE_gt)x⟨g| O_ii exp(-iHt) O_jj |g⟩
#   SZreal=real(Sz)
#   SZimag=imag(Sz)
#   println(file,"$t \t $SZreal \t $SZimag  \t $ii \t $jj ")
#   println("$t \t $SZreal \t $SZimag")

#   #---------------------------------------------------------------------------#
#   t≈ttotal && break
#   psi1 = apply(Kitayev.gates, psi1;cutoff=1e-12,maxdim=1000) #Gate Evolution exp(-iHt)|jj⟩
#   #---------------------------------------------------------------------------#
  
# end