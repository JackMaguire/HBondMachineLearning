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

#########################
# COMMAND LINE SETTINGS #
#########################

parser = argparse.ArgumentParser()

parser.add_argument( "-i", help="Input data file", required=True )
parser.add_argument( "-m", help="Input Model File (h5)", required=True )

args = parser.parse_args()

if( args.i ):
    datafilename = args.i
else:
    print( "The -i argument is required" )
    parser.parse_args( ['-h'] )
    exit( 0 )

model_filename = args.m

#########
# FUNCS #
#########

def my_assert_equals( name, actual, theoretical ):
    if actual != theoretical:
        print( name + " is equal to " + actual + " instead of " + theoretical )
        exit( 1 )


###########
# METRICS #
###########

def mean_pred( y_true, y_pred ):
    return K.mean( y_pred )

#########
# START #
#########

model = load_model( model_filename )

dataset = numpy.genfromtxt( datafilename, delimiter=",", skip_header=0 )
test_input = dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]
test_output_hbond = dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]

#scale hbond scores
for x in test_output_hbond:
    for i in range( 0, len(x) ):
        x[i] *= -1
        if x[i] > 1:
            x[i] = 1

num_elements = len( dataset )

#scores = model.evaluate( test_input, test_output_hbond )
#print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

for i in range( 0, len( dataset ) ):
    #print( test_output_hbond[ i ] )
    #print( "\n" )
    #print( test_output_hbond[ i ][ 0 ] )
    #print( "\n" )
    #print( test_input[ i ] )

    temp_array = numpy.zeros( shape=( 9, 1 ) )
    for j in range( 0, 9 ):
        temp_array[ j ][ 0 ] = test_input[ i ][ j ]

    #print( "\n" )
    #print( temp_array )
    #exit( 0 )
    #print( temp_array.shape )

    actual = test_output_hbond[ i ][ 0 ]
    prediction = model.predict( numpy.transpose( temp_array ) )
    #prediction = model.predict( test_input[ i ][ 0 ] )
    print( str( actual ) + "\t" + str( prediction ) )

