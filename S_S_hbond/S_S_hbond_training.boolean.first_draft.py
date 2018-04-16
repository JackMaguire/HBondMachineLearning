#from keras import *
from keras.models import Sequential
from keras.layers import Dense
from keras import metrics

import keras.backend as K
import keras.callbacks
import keras
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

parser.add_argument( "--train", help="Input data file for training", required=True )
parser.add_argument( "--test", help="Input data file for testing", required=True )

parser.add_argument( "--num_neurons_in_first_hidden_layer", help="Number of neruons for first hidden layer.", default="100", type=int, required=False )
parser.add_argument( "--num_neurons_in_intermediate_hidden_layer", help="Number of neruons for intermediate hidden layer.", default="100", type=int, required=False )
parser.add_argument( "--num_intermediate_hidden_layers", help="Number of intermediate hidden layers.", default="4", type=int, required=False )

parser.add_argument( "--num_epochs", help="Number of epochs to give to model.fit()", default="150", type=int, required=False )
parser.add_argument( "--batch_size", help="Batch size to give to model.fit()", default="10", type=int, required=False )

args = parser.parse_args()

if( args.train ):
    train_datafilename = args.train
else:
    print( "The --train argument is required" )
    parser.parse_args( ['-h'] )
    exit( 0 )

test_datafilename = args.test
print( "test_datafilename: " + test_datafilename )

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

def keep_hbond_score( score ):
    hbond_score = score[ BEST_POSSIBLE_HBOND_SCORE ]
    print( score )
    print( hbond_score )
    exit( 0 )
    if score == 0:
        return true
    if score <= -0.5:
        return true
    return false

###########
# CLASSES #
###########
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

###########
# METRICS #
###########

def mean_pred( y_true, y_pred ):
    return K.mean( y_pred )

#########
# START #
#########

# 1) Generate Data

training_dataset = numpy.genfromtxt( train_datafilename, delimiter=",", skip_header=0 )
#training_dataset = [x for x in training_dataset if keep_hbond_score( x ) ]

training_input = training_dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]
training_output_hbond = training_dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]

for x in training_output_hbond:
    for i in range( 0, len(x) ):
        if x[i] != 0:
            x[i] = 1

my_assert_equals( "len(input)", len(training_input), len(training_output_hbond) )

del training_dataset

test_dataset = numpy.genfromtxt( test_datafilename, delimiter=",", skip_header=0 )
#test_dataset = [x for x in test_dataset if keep_hbond_score( x ) ]

test_input = test_dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]
test_output_hbond = test_dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]

for x in test_output_hbond:
    for i in range( 0, len(x) ):
        if x[i] != 0:
            x[i] = 1

my_assert_equals( "len(input)", len(test_input), len(test_output_hbond) )

del test_dataset

print( "Training on " + str( len (training_input) ) + " elements" )
print( "Testing on "  + str( len (test_input)     ) + " elements" )

# 2) Define Model

num_input_dimensions = len( training_input[0] )
my_assert_equals( "num_input_dimensions", num_input_dimensions, 9 )

model = Sequential()

model.add( Dense( num_neurons_in_first_hidden_layer, input_dim=num_input_dimensions, activation='relu') )

for x in range( 0, num_intermediate_hidden_layers ):
    model.add( Dense( num_neurons_in_intermediate_hidden_layer, activation='relu') )

num_neurons_in_final_layer = int( 1 )
model.add( Dense( num_neurons_in_final_layer, activation='sigmoid') )

# 3) Compile Model

metrics_to_output=[ 'accuracy' ]
model.compile( loss='mean_squared_error', optimizer='adam', metrics=metrics_to_output )

# 4) Fit Model
history = LossHistory()
model.fit( x=training_input, y=training_output_hbond, epochs=num_epochs, batch_size=my_batch_size, shuffle=False, callbacks=[history], validation_data=(test_input, test_output_hbond) )


# 5) Evaluate Model
print(history.losses)

if test_input is None:
    #what should we do here?
    print( "No data to test" )
else:
    scores = model.evaluate( test_input, test_output_hbond )
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# 6) Save Model
model.save( "model.h5" )
