#from keras import *
from keras.models import Sequential
from keras.layers import Dense
from keras import metrics

#import keras
from keras.models import load_model
import keras.backend as K
import numpy

import sys

import argparse

########
# INIT #
########

numpy.random.seed( 0 )

#############
# CONSTANTS #
#############

#13 columns
#best_possible_hbond_score,worst_possible_clash_score,tx,ty,tz,rz,ry,rz,pair,cenpack,angle1,angle2,dist

BEST_POSSIBLE_HBOND_SCORE  = int( 0 )
WORST_POSSIBLE_CLASH_SCORE = int( 1 )

TX = int( 2 )
TY = int( 3 )
TZ = int( 4 )

RX = int( 5 )
RY = int( 6 )
RZ = int( 7 )

PAIR    = int( 8 )
CENPACK = int( 9 )

ANGLE1 = int( 10 )
ANGLE2 = int( 11 )
DIST   = int( 12 )

def generate_data_from_file( filename ):
    dataset = numpy.genfromtxt( filename, delimiter=",", skip_header=0 )

    input = dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]
    output_hbond = dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]

    for x in output_hbond:
        for i in range( 0, len(x) ):
            if x[i] != 0:
                x[i] = 1

    return input, output_hbond

#########################
# COMMAND LINE SETTINGS #
#########################

#first: modelname
#rest: datafile names

model_filename = sys.argv[ 1 ]
model = load_model( model_filename )

num_positives_actual = 0.
num_positives_predicted = 0.
num_positives_actual_and_predicted = 0.

num_negatives_actual = 0.
num_negatives_predicted = 0.
num_negatives_actual_and_predicted = 0.

for h in range( 2, len( sys.argv ) ):

    filename = sys.argv[ h ]
    #print( filename )
    test_input, test_output_hbond = generate_data_from_file( filename )

    for i in range( 0, len(test_input) ):

        temp_array = numpy.zeros( shape=( 9, 1 ) )
        for j in range( 0, 9 ):
            temp_array[ j ][ 0 ] = test_input[ i ][ j ]

        actual = test_output_hbond[ i ][ 0 ]
        prediction = model.predict( numpy.transpose( temp_array ) )[0][0]

        #print( str(actual) + " " + str(prediction) )
        #continue
        if actual == 0:
            num_negatives_actual += 1
            if prediction < 0.5:
                num_negatives_predicted += 1
                num_negatives_actual_and_predicted += 1
            else:
                num_positives_predicted += 1
        else:
            num_positives_actual += 1
            if prediction < 0.5:
                num_negatives_predicted += 1
            else:
                num_positives_actual_and_predicted += 1
                num_positives_predicted += 1

            
print( str(num_positives_actual_and_predicted) + " " +
       str(num_positives_actual) + " " +
       str(num_positives_actual_and_predicted/num_positives_actual) + " " +
       str(num_negatives_actual_and_predicted) + " " +
       str(num_negatives_actual) + " " +
       str(num_negatives_actual_and_predicted/num_negatives_actual)
)

