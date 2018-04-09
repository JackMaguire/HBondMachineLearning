#from keras import *
from keras.models import Sequential
from keras.layers import Dense
from keras import metrics

import keras.backend as K
import numpy

import sys

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

if len( sys.argv ) != 2:
    print( "Lone argument should be data file" )
    exit( 1 )

datafilename = sys.argv[ 1 ]

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

#0 for no hbond
#1 for any hbond at least -0.5 REU in strength
#linear interpolation between
def hbond_score_to_01_scale( hbond_score ):
    if hbond_score >= 0.0:
        return 0
    elif hbond_score <= -0.5:
        return 1
    else:
        return -2.0 * hbond_score

#########
# START #
#########

# 1) Generate Data

dataset = numpy.genfromtxt( datafilename, delimiter=",", skip_header=1 )
#print( len( dataset[ 0 ] ) )

input = dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]

both_output = dataset[:,0:2]
output_hbond = dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]
output_clash = dataset[:,[ WORST_POSSIBLE_CLASH_SCORE ] ]

num_elements = len( dataset )
num_training_elements = int( 0.8 * float( num_elements) )

my_assert_equals( "len(input)", len(input), len(both_output) )

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

num_input_dimensions = len( input[0] );
my_assert_equals( "num_input_dimensions", num_input_dimensions, 9 )

model = Sequential()

num_neurons_in_first_layer = int( 100 )
model.add( Dense( num_neurons_in_first_layer, input_dim=len( input[0] ), activation='relu') )

num_neurons_in_second_layer = int( 100 )
model.add( Dense( num_neurons_in_second_layer, activation='relu') )

num_neurons_in_third_layer = int( 100 )
model.add( Dense( num_neurons_in_third_layer, activation='sigmoid') )

# 3) Compile Model

metrics_to_output=[ 'accuracy' ]
model.compile( loss='mean_squared_error', optimizer='adam', metrics=metrics_to_output )

# 4) Fit Model
num_epochs=150    #150 is small
my_batch_size=10  #10  is small
model.fit( training_input, training_output_hbond, epochs=num_epochs, batch_size=my_batch_size )

# 5) Evaluate Model
scores = model.evaluate( test_input, test_output_hbond )
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# 6) Save Model
model.save( "model.h5" )
