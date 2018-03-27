#from keras import *
from keras.models import Sequential
from keras.layers import Dense
from keras import metrics

import keras.backend as K
import numpy

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

dataset = numpy.genfromtxt( "sample_data.csv", delimiter=",", skip_header=1 )
print( len( dataset[ 0 ] ) )

input = dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]

both_output = dataset[:,0:2]
output_hbond = dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]
output_clash = dataset[:,[ WORST_POSSIBLE_CLASH_SCORE ] ]

# 2) Define Model

num_input_dimensions = len(input[0]);
my_assert_equals( "num_input_dimensions", num_input_dimensions, 9 )

model = Sequential()

num_neurons_in_first_layer = int( 12 )
model.add( Dense( num_neurons_in_first_layer, input_dim=len( input[0] ), activation='relu') )

num_neurons_in_second_layer = int( 8 )
model.add( Dense( num_neurons_in_second_layer, activation='relu') )

num_neurons_in_third_layer = int( 1 )
model.add( Dense( num_neurons_in_third_layer, activation='sigmoid') )

# 3) Compile Model

metrics_to_output=[ ]
model.compile( loss='mean_squared_error', optimizer='adam', metrics=['accuracy'] )
