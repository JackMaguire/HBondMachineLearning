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
import random

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

#parser.add_argument( "--train", help="Input data file for training", required=True )
#parser.add_argument( "--test", help="Input data file for testing", required=True )

parser.add_argument( "--num_neurons_in_first_hidden_layer", help="Number of neruons for first hidden layer.", default="100", type=int, required=False )
parser.add_argument( "--num_neurons_in_intermediate_hidden_layer", help="Number of neruons for intermediate hidden layer.", default="100", type=int, required=False )
parser.add_argument( "--num_intermediate_hidden_layers", help="Number of intermediate hidden layers.", default="4", type=int, required=False )

parser.add_argument( "--num_epochs", help="Number of epochs to give to model.fit()", default="150", type=int, required=False )
parser.add_argument( "--batch_size", help="Batch size to give to model.fit()", default="10", type=int, required=False )

parser.add_argument( "--test_predictions", help="filename for test predictions", default="", required=False )

args = parser.parse_args()

#if( args.train ):
#    train_datafilename = args.train
#else:
#    print( "The --train argument is required" )
#    parser.parse_args( ['-h'] )
#    exit( 0 )

#test_datafilename = args.test
#print( "test_datafilename: " + test_datafilename )

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

test_predictions = args.test_predictions
if( len(test_predictions) > 0 ):
    print( "Will save test predictions to " + test_predictions )
else:
    print( "Will not save test predictions because --test_predictions was not given" )

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

def generate_data_from_file( filename ):
    dataset = numpy.genfromtxt( filename, delimiter=",", skip_header=0 )

    input = training_dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]
    output_hbond = training_dataset[:,[ BEST_POSSIBLE_HBOND_SCORE  ] ]

    for x in output_hbond:
        for i in range( 0, len(x) ):
            if x[i] != 0:
                x[i] = 1

    return input, output_hbond


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

# 1) Define Filenames
input_file_path = "/Volumes/My Book/tensorflow_hbonds_and_clashes/S_S/no_middle_hbond_data/LOG_no_middle_data_split/"
training_input_files = [ "split_aa", "split_ab", "split_ac", "split_ad", "split_ae", "split_af", "split_ag" ]
testing_input_files = [ "split_ah", "split_ai", "split_aj" ]

# 2) Define Model

num_input_dimensions = 9
model = Sequential()

model.add( Dense( num_neurons_in_first_hidden_layer, input_dim=num_input_dimensions, activation='relu') )

for x in range( 0, num_intermediate_hidden_layers ):
    model.add( Dense( num_neurons_in_intermediate_hidden_layer, activation='relu') )

num_neurons_in_final_layer = int( 1 )
model.add( Dense( num_neurons_in_final_layer, activation='sigmoid') )

# 3) Compile Model

metrics_to_output=[ 'accuracy' ]
model.compile( loss='binary_crossentropy', optimizer='adam', metrics=metrics_to_output )

# 4) Fit Model
#history = LossHistory()
#model.fit( x=training_input, y=training_output_hbond, epochs=num_epochs, batch_size=my_batch_size, shuffle=False, callbacks=[history], validation_data=(test_input, test_output_hbond), class_weight={0:1, 1:1000} )

for x in range( 0, num_epochs ):
    random.shuffle( training_input_files )
    for training_input_filename in training_input_files:
        training_input_temp, training_output_hbond_temp = generate_data_from_file( input_file_path + training_input_filename )
        model.train_on_batch( x=training_input_temp, y=training_output_hbond_temp, class_weight={0:1, 1:1000} )
    if ( x % 25 == 0 ):
        model.save( "epoch_" + str(x) + ".h5" )

# 6) Save Model
model.save( "model.h5" )

# 7) Print Predicitons
if( len(test_predictions) > 0 ):
    test_predictions_file = open ( test_predictions, "w" )
    for test_filename in testing_input_files:
        test_input, test_output_hbond = generate_data_from_file( input_file_path + test_filename )
        for i in range( 0, len( test_input ) ):
            temp_array = numpy.zeros( shape=( 9, 1 ) )
            for j in range( 0, 9 ):
                temp_array[ j ][ 0 ] = test_input[ i ][ j ]
            actual = test_output_hbond[ i ][ 0 ]
            prediction = model.predict( numpy.transpose( temp_array ) )
            test_predictions_file.write( str( actual ) + "\t" + str( prediction[0][0] ) + "\n" )

