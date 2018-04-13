#from keras import *
from keras.models import Sequential
from keras.layers import Dense
from keras import metrics

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
parser.add_argument( "--num_neurons_in_first_hidden_layer", help="Number of neruons for first hidden layer.", default="100", type=int, required=False )
parser.add_argument( "--num_neurons_in_intermediate_hidden_layer", help="Number of neruons for intermediate hidden layer.", default="100", type=int, required=False )
parser.add_argument( "--num_intermediate_hidden_layers", help="Number of intermediate hidden layers.", default="4", type=int, required=False )

parser.add_argument( "--num_epochs", help="Number of epochs to give to model.fit()", default="150", type=int, required=False )
parser.add_argument( "--batch_size", help="Batch size to give to model.fit()", default="10", type=int, required=False )

args = parser.parse_args()

if( args.i ):
    datafilename = args.i
else:
    print( "The -i argument is required" )
    parser.parse_args( ['-h'] )
    exit( 0 )

num_neurons_in_first_hidden_layer = args.num_neurons_in_first_hidden_layer
print( "num_neurons_in_first_hidden_layer: " + str( num_neurons_in_first_hidden_layer ) )

num_neurons_in_intermediate_hidden_layer = args.num_neurons_in_intermediate_hidden_layer
print( "num_neurons_in_intermediate_hidden_layer: " + str( num_neurons_in_intermediate_hidden_layer ) )

num_intermediate_hidden_layers = args.num_intermediate_hidden_layers
print( "num_intermediate_hidden_layers: " + str( num_intermediate_hidden_layers ) )

num_epochs = args.num_epochs #150 is small
print( "num_epochs: " + str( num_epochs ) )

my_batch_size = args.batch_size #10 \is small
print( "batch_size: " + str( my_batch_size ) )

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

# 1) Generate Data

dataset = numpy.genfromtxt( datafilename, delimiter=",", skip_header=1 )
#print( len( dataset[ 0 ] ) )

input = dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]

#both_output = dataset[:,0:2]
output_hbond = dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]
#output_clash = dataset[:,[ WORST_POSSIBLE_CLASH_SCORE ] ]

#scale hbond scores
for x in output_hbond:
    for i in range( 0, len(x) ):
        x[i] *= -1
        if x[i] > 1:
            x[i] = 1

num_elements = len( dataset )
num_training_elements = int( 0.8 * float( num_elements) )

my_assert_equals( "len(input)", len(input), len(output_hbond) )

training_input = input[ :num_training_elements, : ]
test_input     = input[ num_training_elements:, : ]

training_output_hbond = output_hbond[ :num_training_elements, : ]
test_output_hbond     = output_hbond[ num_training_elements:, : ]

#training_output_clash = output_clash[ :num_training_elements, : ]
#test_output_clash     = output_clash[ num_training_elements:, : ]

print( "Training on " + str( len (training_input) ) + " elements" )
print( "Testing on "  + str( len (test_input)     ) + " elements" )
#exit( 0 )

# 2) Define Model

num_input_dimensions = len( input[0] )
my_assert_equals( "num_input_dimensions", num_input_dimensions, 9 )

model = Sequential()

#num_neurons_in_nth_layer will have their own variables in case we want to reference them later.
model.add( Dense( num_neurons_in_first_hidden_layer, input_dim=len( input[0] ), activation='relu') )

for x in range( 0, num_intermediate_hidden_layers ):
    model.add( Dense( num_neurons_in_intermediate_hidden_layer, activation='relu') )

num_neurons_in_final_layer = int( 1 )
model.add( Dense( num_neurons_in_final_layer, activation='sigmoid') )

# 3) Compile Model

metrics_to_output=[ 'accuracy' ]
model.compile( loss='mean_squared_error', optimizer='adam', metrics=metrics_to_output )

# 4) Fit Model
model.fit( training_input, training_output_hbond, epochs=num_epochs, batch_size=my_batch_size )

# 5) Evaluate Model
scores = model.evaluate( test_input, test_output_hbond )
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# 6) Save Model
model.save( "model.h5" )
