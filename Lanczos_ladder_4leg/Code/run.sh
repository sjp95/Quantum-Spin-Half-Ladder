#!/usr/bin/env bash
set -e

# Performance tuning for linear algebra / numpy
export MKL_NUM_THREADS=$(nproc)
export OMP_NUM_THREADS=$(nproc)

echo "Starting execution of 4-leg Python qkrylov model..."

for hz in  50 20 80 150
do
 for Jz in {0..150..2}
 do
  python3 st1.py 12 0.0 100.0 $Jz 0.0 0.0 $hz pbc
 done
done

# ==========================================================
# Run DE_gap.py for analyzing energy and gap
# ==========================================================
N=12
for Md in "energy" "gap" "d2"
do
    MODE=$Md
    SWEEP="J2"
    J1=1.0
    J2=0.0

    for hz in  0.5 0.2 0.8 1.5
    do
        HX=0.0
        HY=0.0
        HZ=$hz

        echo "======================================"
        echo "Running DE_gap.py"
        echo "======================================"
        echo "N      = $N"
        echo "MODE   = $MODE"
        echo "SWEEP  = $SWEEP"
        echo "J1     = $J1"
        echo "J2     = $J2"
        echo "HX     = $HX"
        echo "HY     = $HY"
        echo "HZ     = $HZ"
        echo "======================================"

        python3 DE_gap.py \
                $N \
                $MODE \
                $SWEEP \
                $J1 \
                $J2 \
                $HX \
                $HY \
                $HZ

        echo ""
        echo "Finished."
    done
done

# ==========================================================
# Run combine_nematic.py to process Nematic order data
# ==========================================================
N=12
SWEEP="J2"
J1=1.0
J2=0.0

for hz in  0.5 0.2 0.8 1.5
do
        HX=0.0
        HY=0.0
        HZ=$hz

        echo "======================================"
        echo "Running combine_nematic.py"
        echo "======================================"
        echo "N      = $N"
        echo "SWEEP  = $SWEEP"
        echo "J1     = $J1"
        echo "J2     = $J2"
        echo "HX     = $HX"
        echo "HY     = $HY"
        echo "HZ     = $HZ"
        echo "======================================"

        python3 combine_nematic.py \
                $N \
                $SWEEP \
                $J1 \
                $J2 \
                $HX \
                $HY \
                $HZ
        echo ""
        echo "Finished."
done

# ==========================================================
# Run combine_chirality.py to process Chirality data
# ==========================================================
N=12
SWEEP="J2"
J1=1.0
J2=1.0

for hz in  0.5 0.2 0.8 1.5
do
    HX=0.0
    HY=0.0
    HZ=$hz

    echo "======================================"
    echo "Running combine_chirality.py"
    echo "======================================"
    echo "N      = $N"
    echo "SWEEP  = $SWEEP"
    echo "J1     = $J1"
    echo "J2     = $J2"
    echo "HX     = $HX"
    echo "HY     = $HY"
    echo "HZ     = $HZ"
    echo "======================================"

    python3 combine_chirality.py \
            $N \
            $SWEEP \
            $J1 \
            $J2 \
            $HX \
            $HY \
            $HZ

    echo ""
    echo "Finished."
done
