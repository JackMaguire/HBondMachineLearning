#!/bin/bash

aas=DEHKNQRSTWY

for x in `seq 0 10`; do
    aa1=${aas:$x:1}
    for y in `seq $x 10`; do
	aa2=${aas:$y:1}

	if [ -f /nas/longleaf/home/jackmag/pine/tensorflow_hbonds/randomly_generated_data/${aa1}_${aa2}/training.dat ]; then
	    sbatch -t "0-1" --mem-per-cpu=1000 -o LOG.${aa1}_${aa2} ~/dummy.sh bash test_all.sh $aa1 $aa2
	fi

    done
done
