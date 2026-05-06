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
  Kitayev.Jz = parse(Float64, ARGS[3])
  # order = parse(Int64, ARGS[4])
  Kitayev.hz = parse(Float64, ARGS[4])
  Kitayev.longrange = 1
  Kitayev.sites = siteinds("tJ",N;conserve_qns=false)
  #===========================================================================#
  #===========================================================================#

  #===========================================================================#
        #================= Printing of Parameters ===================#
  #===========================================================================#
  
  Kitayev.Values()
  Kitayev.printMatrix(Kitayev.JJx)
  Kitayev.printMatrix(Kitayev.JJz)

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
  cutoff = [1E-10]
  energy, psi = dmrg(H, psi0; nsweeps, maxdim, cutoff, noise)
  println("\n Groundstate Energy: $energy \n")
  #===========================================================================#
  #===========================================================================#

  #===========================================================================#
  #===========================================================================#
  magz = expect(psi,"Sz")
  magx = expect(psi,"Sx")
  zzcorr1 = correlation_matrix(psi,"Sx","Sx")
  zzcorrz = correlation_matrix(psi,"Sz","Sz")
  
  #===========================================================================#
  #===========================================================================#
  file_name = "New"
  Kitayev.Make_Directory("../Data")
  Kitayev.Make_Directory("../Data/Correlations")
  Kitayev.Make_Directory("../Data/Magnetization")
  Kitayev.Make_Directory("../Data/MPS")
  Kitayev.Make_Directory("../Data/Energy")
  #===========================================================================#
  #===========================================================================#

  #===========================================================================#
                        #============Save MPS============#
  #===========================================================================#
  Jx = Int(Kitayev.Jx * 100)
  Jz = Int(Kitayev.Jz * 100)
  hz = Int(Kitayev.hz * 100)
  using HDF5
  file_nameMPS = "../Data/MPS/SZ_$(Kitayev.N)_$(Jx)_$(Jz)_$(hz).h5"
  f = h5open(file_nameMPS,"w")  
  write(f,"psi",psi)
  close(f)
  #===========================================================================#
  #===========================================================================#
  file_name = "../Data/Correlations/SZ_$(Kitayev.N)_$(Jx)_$(Jz)_$(hz).dat"
  file_name1 = "../Data/Magnetization/SZ_$(Kitayev.N)_$(Jx)_$(Jz)_$(hz).dat"
  file_name2 = "../Data/Magnetization/SX_$(Kitayev.N)_$(Jx)_$(Jz)_$(hz).dat"
  file_name3 = "../Data/Magnetization/M_$(Kitayev.N)_$(Jx)_$(Jz)_$(hz).dat"
  file_name4 = "../Data/Energy/E_$(Kitayev.N)_$(Jx)_$(Jz)_$(hz).dat"
  #===========================================================================#
  #===========================================================================#
  file = open(file_name, "w")
  file1 = open(file_name1, "w")
  file2 = open(file_name2, "w")
  file3 = open(file_name3, "w")
  file4 = open(file_name4, "w")
  #===========================================================================#
  #===========================================================================#
  mz00=0
  mx00=0
  for i in 1:Kitayev.N
    #===========================================================================#
    for j in 1:Kitayev.N
      #===========================================================================#
          println(file, "$i  $j  $(zzcorr1[i,j])  $(zzcorrz[i,j]) $(magx[i]*magx[j]) $(magz[i]*magz[j])")
    
      #===========================================================================#
    end
    #===========================================================================#
    println(file, "\n")
    println(file1, "$i  $(magz[i])")
    println(file2, "$i  $(magx[i])")
    mz00+=magz[i]/Kitayev.N
    mx00+=magx[i]/Kitayev.N
  end
  println(file3, "$(Kitayev.hz)  $(Kitayev.Jx)  $(Kitayev.Jz)  $(mz00)  $(mx00)")
  println(file4, "$(Kitayev.hz)  $(Kitayev.Jx)  $(Kitayev.Jz)  $(energy)")
  #===========================================================================#
  close(file)
  close(file1)
  close(file2)
  close(file3)
  #===========================================================================#
  #===========================================================================#
  return
end
