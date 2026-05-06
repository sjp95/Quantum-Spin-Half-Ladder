#ifndef NSCORDER_HPP_INCLUDED
#define NSCORDER_HPP_INCLUDED

#include "input.hpp"
#include "order0.hpp"
#include "order1.hpp"
#include "order2.hpp"

#include "SQ0.hpp"
#include "SQ1.hpp"
#include "SQ2.hpp"

#include "consolidate.hpp"

using namespace std;
using namespace Eigen;


void NSC_input::Data_of_order(int ii)
{
    if (ii==0)
    {
        order0_data();
        Sq0();
    }
    if (ii==1)
    {
        order1_data();
        Sq1();
    }
    if (ii==2)
    {
        order2_data();
        Sq2();
    }
    
}

#endif