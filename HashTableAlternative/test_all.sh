#!/bin/bash

for x in 15 20 25 50; do
    java CreateTable /nas/longleaf/home/jackmag/pine/tensorflow_hbonds/native_data/Y.Y.nonnative.csv.no_middle_data.csv,/nas/longleaf/home/jackmag/pine/tensorflow_hbonds/randomly_generated_data/Y_Y/training.dat temp.y_y.dat $x
    java EvaluateTable temp.y_y.dat /nas/longleaf/home/jackmag/pine/tensorflow_hbonds/randomly_generated_data/Y_Y/testing.dat /nas/longleaf/home/jackmag/pine/tensorflow_hbonds/native_data/Y.Y.native.csv #| sort -nk6 | tail -n1 | awk '{print $6}'
done | sort -nk6 | tail -n1 | awk '{print $6}'
