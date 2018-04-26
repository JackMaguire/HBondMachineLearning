import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from pyrosetta import *
init()
from pyrosetta.teaching import *
from pyrosetta.rosetta.protocols.data_generation.hbond_machine_learning import *

#from keras import *
from keras.models import Sequential
from keras.layers import Dense
from keras import metrics

from keras.models import load_model
import keras.backend as K
import keras.callbacks
import keras
import numpy

import sys
sys.path.append("/nas/longleaf/home/jackmag")#for h5py
import h5py

import argparse
import random
import time

########
# INIT #
########

numpy.random.seed( 0 )

#########################
# COMMAND LINE SETTINGS #
#########################

parser = argparse.ArgumentParser()

parser.add_argument( "--input_model", help="Model to start out with", required=True )

parser.add_argument( "--aa1", help="First Amino Acid 1-letter Code", required=True )
parser.add_argument( "--aa2", help="Second Amino Acid 1-letter Code", required=True )

parser.add_argument( "--num_epochs", help="Number of epochs to give to model.fit()", default="150", type=int, required=False )

parser.add_argument( "--weight", help="Class weight for 1", default="3.0", required=True )

parser.add_argument( "--infinite_loop", help="If 1, will run until stopped", default="0", type=int, required=False )

args = parser.parse_args()

input_model_filename = args.input_model
print( "input_model: " + input_model_filename )

aa1 = args.aa1
print( "aa1: " + aa1 )

aa2 = args.aa2
print( "aa2: " + aa2 )

num_epochs = args.num_epochs #150 is small
print( "num_epochs: " + str( num_epochs ) )

weight1 = args.weight
print( "class weight for 1: " + str( weight1 ) );

infinite_loop = str( args.infinite_loop ) == "1"
print( "infinite_loop: " + str(infinite_loop) )

#########
# FUNCS #
#########

def my_assert_equals( name, actual, theoretical ):
    if actual != theoretical:
        print( name + " is equal to " + actual + " instead of " + theoretical )
        exit( 1 )

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

def evaluate_model( model, best_score_so_far, test_input, test_output_hbond, batch ):
    num_positives_actual = 0.
    num_positives_predicted = 0.
    num_positives_actual_and_predicted = 0.

    num_negatives_actual = 0.
    num_negatives_predicted = 0.
    num_negatives_actual_and_predicted = 0.
        
    predictions = model.predict( x=test_input );

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

    min = 1;
    score1 = num_positives_actual_and_predicted/num_positives_actual
    score2 = num_negatives_actual_and_predicted/num_negatives_actual
    if score1 < min:
        min = score1
    if score2 < min:
        min = score2

    saved = 0

    if min >= best_score_so_far:
        best_score_so_far = min
        model.save( "best2.h5" )
        saved = 1

    print( str(batch) + " " + str(score1) + " " + str(score2) + " " + str(saved) )

    return best_score_so_far

def generate_N_elements( N, generator ):
    #returns numpy arrays of dimension (N,9) and (N,1)
    input = numpy.empty( [ N, 9 ], dtype=float )
    output_hbond = numpy.empty( [ N, 1 ], dtype=float )
    for i in range( 0, N ):
        data = generator.get_sample()
        while ( data.Lowest_HBNet_Score < 0 and data.Lowest_HBNet_Score > -0.5 ):
            data = generator.get_sample()

        input[ i ][ 0 ] = data.Tx
        input[ i ][ 1 ] = data.Ty
        input[ i ][ 2 ] = data.Tz
        input[ i ][ 3 ] = data.Rx
        input[ i ][ 4 ] = data.Ry
        input[ i ][ 5 ] = data.Rz
        input[ i ][ 6 ] = data.Theta1
        input[ i ][ 7 ] = data.Theta2
        input[ i ][ 8 ] = data.D
        normalize_single_input( input[ i ] )

        if data.Lowest_HBNet_Score == 0:
            output_hbond[ i ][ 0 ] = 0
        else:
            output_hbond[ i ][ 0 ] = 1

    return input, keras.utils.to_categorical( output_hbond, num_classes=2 )
    #return input, output_hbond


#https://stackoverflow.com/questions/4601373/better-way-to-shuffle-two-numpy-arrays-in-unison
def shuffle_in_unison(a, b):
    rng_state = numpy.random.get_state()
    numpy.random.shuffle(a)
    numpy.random.set_state(rng_state)
    numpy.random.shuffle(b)

def print_data( input, output_hbond ):
    print( " " )
    my_assert_equals( "print_data() input sizes", len(input), len(output))
    for x in len( input ):
        out_string = str(output[x][0]) + ",0"
        for y in output[x]:
            out_string += "," + str(y)
        print( out_string )

###########
# CLASSES #
###########

#initially copied from https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly.html
class DataGenerator(keras.utils.Sequence):

    def __init__( self, hbond_data_generator, batch_size=1000, batches_per_epoch=10 ):
        self.batch_size = batch_size
        self.batches_per_epoch = batches_per_epoch
        self.len = batches_per_epoch * batch_size
        self.hbond_data_generator = hbond_data_generator

    def __len__(self):
        'Denotes the number of batches per epoch'
        return self.len

    def __getitem__(self, index):
        'Generate one batch of data'
        X, y = generate_N_elements( self.batch_size, self.hbond_data_generator )
        return X, y

    def on_epoch_end(self):
        pass        

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

if os.path.isfile( input_model_filename ):
    model = load_model( input_model_filename )
else:
    print( "No file with path: " + input_model_filename )
    exit( 1 )

exit( 1 )

testing_input = numpy.load( "testing.dat.input.npy" )
testing_output_hbond = numpy.load( "testing.dat.hbond.npy" )


# 4) Fit Model
hbond_data_generator = pyrosetta.rosetta.protocols.data_generation.hbond_machine_learning.HBondDataGenerator()
hbond_data_generator.init( aa1[0], aa2[0] )

best_score_so_far = 0
best_score_so_far = evaluate_model( model, best_score_so_far, testing_input, testing_output_hbond, 0 )

x = 0
while x < num_epochs:
    start = time.time()
    print( "Beginning epoch: " + str(x) )
    
    training_input, training_output_hbond = generate_N_elements( 10000, hbond_data_generator )
    model.train_on_batch( x=training_input, y=training_output_hbond, class_weight={ 0 : 1, 1 : weight1 } )

    if ( x % 25 == 0 ):
        best_score_so_far = evaluate_model( model, best_score_so_far, testing_input, testing_output_hbond, x )
        if ( x % 100 == 0 ):
            model.save( "epoch_" + str(x) + ".h5" )

    end = time.time()
    print( "\tseconds: " + str( end - start ) )
    sys.stdout.flush()
    if not infinite_loop:
        x += 1

model.save( "final.h5" )

