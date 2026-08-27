#!/usr/bin/env bash
set -e

N=12
SWEEP="J2"
FIX_PARAMETER="hz"
FIX_VALUES="0.0, 0.04, 0.1, 0.5, 0.8, 1.5"

J1=1.0
J2=1.0
HX=0.0
HY=0.0
HZ=0.0

echo "======================================"
echo "Running PlotObservables.py"
echo "======================================"
echo "N              = $N"
echo "SWEEP          = $SWEEP"
echo "FIX_PARAMETER  = $FIX_PARAMETER"
echo "FIX_VALUES     = $FIX_VALUES"
echo "J1             = $J1"
echo "J2             = $J2"
echo "HX             = $HX"
echo "HY             = $HY"
echo "HZ             = $HZ"
echo "======================================"

python3 PlotObservables.py \
        $N \
        $SWEEP \
        $FIX_PARAMETER \
        "$FIX_VALUES" \
        $J1 \
        $J2 \
        $HX \
        $HY \
        $HZ

echo ""
echo "Finished."
