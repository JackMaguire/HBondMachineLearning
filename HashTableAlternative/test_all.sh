#!/bin/bash

aa1=$1
aa2=$2

for x in 15 20 25 50; do
    java CreateTable /nas/longleaf/home/jackmag/pine/tensorflow_hbonds/native_data/$aa1.$aa2.nonnative.csv.no_middle_data.csv,/nas/longleaf/home/jackmag/pine/tensorflow_hbonds/randomly_generated_data/${aa1}_${aa2}/training.dat temp.${aa1}_${aa2}.dat $x
    java EvaluateTable temp.${aa1}_${aa2}.dat /nas/longleaf/home/jackmag/pine/tensorflow_hbonds/randomly_generated_data/${aa1}_${aa2}/testing.dat /nas/longleaf/home/jackmag/pine/tensorflow_hbonds/native_data/$aa1.$aa2.native.csv #| sort -nk6 | tail -n1 | awk '{print $6}'
done | sort -nk6 | tail -n1 | awk '{print $6}'
