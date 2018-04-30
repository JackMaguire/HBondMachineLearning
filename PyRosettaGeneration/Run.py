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
import subprocess

########
# INIT #
########

numpy.random.seed( 0 )

#Get sha1
pwd = os.path.realpath(__file__)
HBondMachineLearning_index = pwd.find( "HBondMachineLearning" )
path = pwd[:HBondMachineLearning_index]
full_name = "~/HBondMachineLearning/.git".replace( "~", path )
sha1 = subprocess.check_output(["git", "--git-dir", full_name, "rev-parse", "HEAD"]).strip()
print ( "JackMaguire/HBondMachineLearning: " + sha1 )

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
    ppv = num_positives_actual_and_predicted/num_positives_actual
    npv = num_negatives_actual_and_predicted/num_negatives_actual
    if ppv < min:
        #pos_is_limiting_factor = True
        min = ppv
    if npv < min:
        #pos_is_limiting_factor = False
        min = npv

    saved = 0

    if min >= best_score_so_far:
        best_score_so_far = min
        model.save( "gen_best2.h5" )
        saved = 1

    ratio = float(1.0-ppv)/float(1.0-npv)

    print( str(batch) + " " + str(ppv) + " " + str(npv) + " " + str(saved) + " " + str(ratio) )

    return best_score_so_far, ppv, npv

def history_is_increasing( ratio_history ):
    num_ratios = len( ratio_history )
    most_recent_ratio = ratio_history[ num_ratios - 1 ]
    for x in range( 0, num_ratios - 1 ):
        if ratio_history[ x ] >= most_recent_ratio:
            return False
    return True

def history_is_decreasing( ratio_history ):
    num_ratios = len( ratio_history )
    most_recent_ratio = ratio_history[ num_ratios - 1 ]
    for x in range( 0, num_ratios - 1 ):
        if ratio_history[ x ] <= most_recent_ratio:
            return False
    return True

def update_positive_bias_coeff( positive_bias_coeff, ratio_history, min_val, max_val ):
    #figure out if the ratio is good enough
    most_recent_ratio = ratio_history[ len(ratio_history) - 1 ]
    if most_recent_ratio > 0.2 and most_recent_ratio < 5:
        return positive_bias_coeff

    #figure out which direction we need to move to
    if most_recent_ratio < 1:#bias is too large
        if positive_bias_coeff == min_val:
            return positive_bias_coeff
        elif history_is_increasing( ratio_history ):#let the dust settle first
            return positive_bias_coeff
        else:
            return positive_bias_coeff - 0.1#maybe make this step size more dynamic?
    else:#bias is too small
        if positive_bias_coeff == max_val:
            return positive_bias_coeff
        elif history_is_decreasing( ratio_history ):
            return positive_bias_coeff
        else:
            return positive_bias_coeff + 0.1

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
            #print( "!!!" )
            #exit( 0 )
            output_hbond[ i ][ 0 ] = 1

    #return input, keras.utils.to_categorical( output_hbond, num_classes=2 )
    return input, output_hbond


#https://stackoverflow.com/questions/4601373/better-way-to-shuffle-two-numpy-arrays-in-unison
def shuffle_in_unison(a, b):
    rng_state = numpy.random.get_state()
    numpy.random.shuffle(a)
    numpy.random.set_state(rng_state)
    numpy.random.shuffle(b)

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

testing_input = numpy.load( "testing.dat.input.npy" )
testing_output_hbond = numpy.load( "testing.dat.hbond.npy" )


# 4) Fit Model
hbond_data_generator = pyrosetta.rosetta.protocols.data_generation.hbond_machine_learning.HBondDataGenerator()
hbond_data_generator.init( aa1[0], aa2[0] )

best_score_so_far = 0
best_score_so_far, ppv, npv = evaluate_model( model, best_score_so_far, testing_input, testing_output_hbond, 0 )

num_pos_points = 0
num_neg_points = 0

positive_bias_coeff = 10
#ratio_history = [ -1.0, -1.0, -1.0, -1.0, -1.0 ]
#dynamic_bias_offset = 25

x = 0
while x < num_epochs:
    start = time.time()
    print( "Beginning epoch: " + str(x) )
    
    training_input, training_output_hbond = generate_N_elements( 100000, hbond_data_generator )
    for y in training_output_hbond:
        if y[ 0 ] == 0 :
            num_neg_points += 1
        else:
            num_pos_points += 1

    if num_pos_points > 100 and num_neg_points > 1000:
        weight1 = positive_bias_coeff * float( num_neg_points ) / float( num_pos_points )
        print( "updating weight to: " + str(weight1) )

    model.train_on_batch( x=training_input, y=training_output_hbond, class_weight={ 0 : 1, 1 : weight1 } )

    if ( x % 25 == 0 or True ):
        best_score_so_far, ppv, npv = evaluate_model( model, best_score_so_far, testing_input, testing_output_hbond, x )
        '''
        ratio = float(1.0-ppv)/float(1.0-npv)
        ratio_history.pop( 0 )
        ratio_history.append( ratio )
        if dynamic_bias_offset == 0:
            old_bias = positive_bias_coeff
            positive_bias_coeff = update_positive_bias_coeff( positive_bias_coeff, ratio_history, 1.0, 100.0 )
            print ( "updating positive_bias_coeff from " + str( old_bias ) + " to " + str( positive_bias_coeff ) )
        else:
            dynamic_bias_offset -= 1
        '''
        if ( x % 100 == 0 ):
            model.save( "gen_epoch_" + str(x) + ".h5" )

    end = time.time()
    print( "\tseconds: " + str( end - start ) )
    sys.stdout.flush()

    if infinite_loop and x == 24:
            x = 0
    else:
        x += 1

model.save( "gen_final.h5" )

#best_score_so_far = evaluate_model( model, best_score_so_far, cached_testing_input, cached_training_output_hbond, num_epochs )
