#ifndef INSIDE_HPP_INCLUDED
#define INSIDE_HPP_INCLUDED
#include "../input.hpp"
#include <Eigen/Dense>
using namespace std;
using namespace Eigen;

//===================================================================================================//
                                    //=== Inside the cluster Hoping ===//
//===================================================================================================//


// void input::insidehoping( int i)
// {
//     int n = i;
//     for(int k1=0; k1<N;k1++)
//     for(int k2=k1+1; k2<N;k2++)
//     if(abs(Jx(k1,k2))>0)
//     {
//         int id1 =0, id2=0;
//         long long bi=0;
//         for ( int j =0; j<N; j++)
//         {
//             int reminder = i%Ls;
//             i=i/Ls;
//             //======================//
//             if(j==k1)
//             {
                
//                 if (reminder>0)
//                 {
//                     reminder-=1;
//                     id1++;
//                 }
//                 else
//                 {
//                     reminder+=1;
//                     id2++;
//                 }
                
//             }
//             if(j==k2)
//             {
                
//                 if (reminder<Ls-1)
//                 {
//                     reminder+=1;
//                     id2++;
//                 }
//                 else
//                 {
//                     reminder-=1;
//                     id1++;
//                 }

//             }
//             //======================//
//             bi+=reminder*pow(Ls,j);
//         }
//         //double sss=double(id1*id2);
//         int q = int (bi);
//         if(q!=n)
//         {
//             // if(sss>0)
//             // {
//                 H(q,n)=Jx(k1,k2)*0.25;
//                 H(n,q)=conj(H(q,n));
//             //}
//         }
        
//         i=n;
//     }
// }

void input::insidehoping(int state)
{
    std::vector<int> spin(N);

    int temp = state;

    for(int j=0;j<N;j++)
    {
        spin[j] = temp % Ls;
        temp /= Ls;
    }

    for(int k1=0;k1<N;k1++)
    {
        for(int k2=k1+1;k2<N;k2++)
        {
            if(abs(Jx(k1,k2)) == 0.0)
                continue;

            auto newspin = spin;

            // Exact original logic
            if(newspin[k1] > 0)
                newspin[k1]--;
            else
                newspin[k1]++;

            if(newspin[k2] < Ls-1)
                newspin[k2]++;
            else
                newspin[k2]--;

            int q = 0;

            for(int j=0;j<N;j++)
                q += newspin[j] * Lspow[j];

            if(q != state)
            {
                H(q,state) = 0.25 * Jx(k1,k2);
                H(state,q) = std::conj(H(q,state));
            }
        }
    }
}
//===========================================================================================//
//===========================================================================================//
#endif
