#using ITensors, ITensorMPS
module Kitayev
using Base.Filesystem
using ITensors, ITensorMPS
#===========================================================================#
             #================== Parameters ==================#
#===========================================================================#
export N, Jx, Jy, JJx, JJz,hz, longrange, sites

N = 4  # Change this to the desired size
Jx=1
Jz=1
hz=5
longrange=1
sites = siteinds("tJ",N;conserve_qns=false)

JJx = zeros(Float64, N, N)
JJz = zeros(Float64, N, N)

sites = siteinds("S=1/2",N;conserve_qns=false)
gates = ITensor[]

#===========================================================================#
    #================== Function to take the values ==================#
#===========================================================================#
function Resize()
        global JJx = zeros(Float64, N, N)
        global JJz = zeros(Float64, N, N)
    end
#===========================================================================#
#===========================================================================#
function Values()
    Resize()
    for i in 1:N
        if(i<N)
            if(i%2==1)
                JJz[i,i+1]=Jz
                JJz[i+1,i]=Jz

                if i+3 <= N
                    JJx[i,i+3]=Jx
                    JJx[i+3,i]=Jx
                end
            else
                JJx[i,i+1]=Jx
                JJx[i+1,i]=Jx
            end
        end

    end
end
#===========================================================================#
#===========================================================================#
function printMatrix(H0)
    rows, cols = size(H0)
    for i in 1:rows
        for j in 1:cols
          print(H0[i,j], "\t")
        end
        print("\n")
      end
print("\n")
end
#===========================================================================#
#===========================================================================#

function Make_Directory(directory_path)
    if !isdir(directory_path)
        # Create the directory
        mkdir(directory_path)
    else
        println("Directory already exists: $directory_path")
    end
end
#===========================================================================#
#===========================================================================#

# #===========================================================================#
#       #================== Hamiltonian as an MPO ==================#
# #===========================================================================#
function Hamiltonian()
    #global sites = siteinds("tJ",N;conserve_qns=false)
    os = OpSum()
    for j=1:N-1
        if(j%2==1)
            os += JJz[j,j+1]*0.25,"Sz",j,"Sz",j+1 # with propar sx 
            if j+3 <= N
                # os += JJx[j,j+3]*0.25,"S+",j,"S-",j+3
                # os += JJx[j,j+3]*0.25,"S-",j,"S+",j+3
                # os += JJx[j,j+3]*0.25,"S+",j,"S+",j+3
                # os += JJx[j,j+3]*0.25,"S-",j,"S-",j+3
                os += JJx[j,j+3],"Sx",j,"Sx",j+3 # with propar sx
            end
        else
            # os += JJx[j,j+1]*0.25,"S+",j,"S-",j+1
            # os += JJx[j,j+1]*0.25,"S-",j,"S+",j+1
            # os += JJx[j,j+1]*0.25,"S+",j,"S+",j+1
            # os += JJx[j,j+1]*0.25,"S-",j,"S-",j+1
            os += JJx[j,j+1],"Sx",j,"Sx",j+1
        end
        
        os += -hz,"Sz",j,"I",j+1
    end
    os += -hz,"Sz",N,"I",N-1
    H = MPO(os,sites)
    return H
end
#===========================================================================#
#===========================================================================#


#====================================================================================#
          #================== Operators as an MPO ==================#
#====================================================================================#
function Operators(order,ii)
    os1 = OpSum()

    for i in ii-longrange:ii+longrange



        if order==0


            #---------------------------#
            if i==ii-longrange
                os1 += 0.5,"Sx", ii
            end
            #---------------------------#


        elseif order ==1


            #-------------------------------------------------------------------
            if i >= 1  && i <= N

                if abs(JJx[ii, i]+JJz[ii, i]) > 0.0
                    #---------------------------------------------------------------
                    os1 += (JJx[ii, i]+JJz[ii, i])*0.5,"S+",ii,"S+",i; 
                    # os1 += JJx[ii, i]*0.5,"Sz",ii,"S-",ii,"S+",i;

                    # os1 += JJx[ii, i],"Sz",ii,"Sz",ii,"Sz",i;
                    #---------------------------------------------------------------
                end
            end
            #------------------------------------------------------------------

        elseif order ==2


            for kpp in ii-longrange:ii+longrange


                #-------------------------------------------------------------------
                if i >= 1 && abs(JJx[ii, i]*JJz[ii,kpp]) > 0.0 && i <= N

                    #---------------------------------------------------------------
                    os1 += JJx[ii, i]*JJz[ii,kpp]*0.5,"Sz",ii,"S+",i,"S-",kpp; 
                    os1 += JJx[ii, i]*JJz[ii,kpp]*0.5,"Sz",ii,"S-",i,"S+",kpp;

                    os1 += JJx[ii, i]*JJz[ii,kpp],"Sz",ii,"Sz",i,"Sz",kpp;
                    #---------------------------------------------------------------

                end
                #-------------------------------------------------------------------


            end



        end


    end

    O1=MPO(os1,sites)
    return O1
end
#====================================================================================#
#====================================================================================#




#===========================================================================#
            #================== TEBD GATES ==================#
#===========================================================================#
function TEBD_gates(tau)

    gates = ITensor[]

    for j in 1:(N - 1)
        s1 = sites[j]
        s2 = sites[j + 1]
        hj = (JJx[j,j+1]+JJy[j,j+1])*0.25* op("S+", s1) * op("S-", s2) +
             (JJx[j,j+1]+JJy[j,j+1])*0.25* op("S-", s1) * op("S+", s2) +
             (JJx[j,j+1]-JJy[j,j+1])*0.25* op("S+", s1) * op("S+", s2) +
             (JJx[j,j+1]-JJy[j,j+1])*0.25* op("S-", s1) * op("S-", s2)- hz * op("Sz", s1)*op("Id", s2)
        if j==N-1
            hj+=- hz * op("Sz", s2)*op("Id", s1)
        end
        Gj = exp(-im * tau / 2 * hj)
        push!(gates, Gj)
      end
    #   s1 = sites[N-1]
    #   s2 = sites[N]
    #   hj =- hz * op("Sz", s2)*op("Id", s1)
    #   Gj = exp(-im * tau / 2 * hj)
    #   push!(gates, Gj)
      # Include gates in reverse order too
      # (N,N-1),(N-1,N-2),...
      append!(gates, reverse(gates))
      return gates
end
#===========================================================================#
#===========================================================================#




end
using .Kitayev
#using .Kitayev.Operators
