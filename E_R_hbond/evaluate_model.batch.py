#from keras import *
from keras.models import Sequential
from keras.layers import Dense
from keras import metrics

#import keras
from keras.models import load_model
import keras.backend as K
import numpy

import sys
import os.path
import argparse

########
# INIT #
########

numpy.random.seed( 0 )

#############
# CONSTANTS #
#############

#0                         1                          2  3  4  5  6  7  8      9      10
#best_possible_hbond_score,worst_possible_clash_score,tx,ty,tz,rz,ry,rz,angle1,angle2,dist

BEST_POSSIBLE_HBOND_SCORE  = int( 0 )
WORST_POSSIBLE_CLASH_SCORE = int( 1 )

TX = int( 2 )
TY = int( 3 )
TZ = int( 4 )

RX = int( 5 )
RY = int( 6 )
RZ = int( 7 )

ANGLE1 = int( 8 )
ANGLE2 = int( 9 )
DIST   = int( 10 )

def normalize_single_input( input ):
    input[0] /= 20. #Tx
    input[1] /= 20. #Ty
    input[2] /= 20. #Tz
        
    input[3] /= 3.14 #Rx
    input[4] /= 3.14 #Ry
    input[5] -= 1.6  #Rz

    input[6] -= 1.6 #Theta1
    input[7] -= 1.6 #Theta2
    input[8] = (input[8]/15.) - 1 #D

def generate_data_from_file( filename ):
    dataset = numpy.genfromtxt( filename, delimiter=",", skip_header=0 )

    input = dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]
    output_hbond = dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]

    for x in output_hbond:
        for i in range( 0, len(x) ):
            if x[i] > 0:
                print( "Some hbond value is positive! " + str(x[i]) )
                exit( 1 )
            if x[i] != 0:
                x[i] = 1
     
    for x in input:
        normalize_single_input( x )
   
    return input, output_hbond

def replace_last_instance_of_substring(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)

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

    input_cache_filename = filename + ".input.npy"
    hbond_cache_filename = filename + ".hbond.npy"

    input_cache_filename = replace_last_instance_of_substring( input_cache_filename, "/", "/_" )
    hbond_cache_filename = replace_last_instance_of_substring( hbond_cache_filename, "/", "/_" )

    if os.path.isfile( input_cache_filename ) and os.path.isfile( hbond_cache_filename ):
        test_input = numpy.load( input_cache_filename )
        test_output_hbond = numpy.load( hbond_cache_filename )
    else:
        test_input, test_output_hbond = generate_data_from_file( filename )
        numpy.save( input_cache_filename, test_input )
        numpy.save( hbond_cache_filename, test_output_hbond )
        
    predictions = model.predict( x=test_input );

    #print( str(len(test_input)) + " " + str(len(predictions)))
    for i in range( 0, len(test_input) ):

        actual = test_output_hbond[ i ][ 0 ]
        prediction = predictions[ i ][ 0 ]

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

