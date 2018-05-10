# (c) Copyright Rosetta Commons Member Institutions.
# (c) This file is part of the Rosetta software suite and is made available under license.
# (c) The Rosetta software is developed by the contributing members of the Rosetta Commons.
# (c) For more information, see http://www.rosettacommons.org. Questions about this can be
# (c) addressed to University of Washington CoMotion, email: license@uw.edu.

#disable gpu
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

#rosetta
from pyrosetta import *
init()
from pyrosetta.teaching import *
from pyrosetta.rosetta.protocols.data_generation.hbond_machine_learning import *

#Keras
from keras.models import Sequential
from keras.layers import Dense
from keras import metrics
from keras.models import load_model
import keras.backend as K

#other
import numpy
import sys
import os.path
import argparse

########
# INIT #
########

#numpy.random.seed( 0 )
model_names = []
model_names.append( "D_H" )
model_names.append( "D_K" )
model_names.append( "D_N" )
model_names.append( "D_Q" )
model_names.append( "D_R" )
model_names.append( "D_S" )
model_names.append( "D_T" )
model_names.append( "D_W" )
model_names.append( "D_Y" )
model_names.append( "E_H" )
model_names.append( "E_K" )
model_names.append( "E_N" )
model_names.append( "E_Q" )
model_names.append( "E_R" )
model_names.append( "E_S" )
model_names.append( "E_T" )
model_names.append( "E_W" )
model_names.append( "E_Y" )
model_names.append( "H_H" )
model_names.append( "H_K" )
model_names.append( "H_N" )
model_names.append( "H_Q" )
model_names.append( "H_R" )
model_names.append( "H_S" )
model_names.append( "H_T" )
model_names.append( "H_W" )
model_names.append( "H_Y" )
model_names.append( "K_N" )
model_names.append( "K_Q" )
model_names.append( "K_S" )
model_names.append( "K_T" )
model_names.append( "K_Y" )
model_names.append( "N_N" )
model_names.append( "N_Q" )
model_names.append( "N_R" )
model_names.append( "N_S" )
model_names.append( "N_T" )
model_names.append( "N_W" )
model_names.append( "N_Y" )
model_names.append( "Q_Q" )
model_names.append( "Q_R" )
model_names.append( "Q_S" )
model_names.append( "Q_T" )
model_names.append( "Q_W" )
model_names.append( "Q_Y" )
model_names.append( "R_S" )
model_names.append( "R_T" )
model_names.append( "R_Y" )
model_names.append( "S_S" )
model_names.append( "S_T" )
model_names.append( "S_W" )
model_names.append( "S_Y" )
model_names.append( "T_T" )
model_names.append( "T_W" )
model_names.append( "T_Y" )
model_names.append( "W_Y" )
model_names.append( "Y_Y" )

all_models = {}

for model_name in model_names:
    filename_for_model = pyrosetta.rosetta.basic.database.find_database_path( "protocol_data/hbond_machine_learning/models/", model_name + ".h5" )
    all_models[ model_name ] = load_model( filename_for_model )

hbond_data_generator = pyrosetta.rosetta.protocols.data_generation.hbond_machine_learning.HBondDataGenerator()

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

def create_input_tensor( residue1, residue2 ):
    DEBUG = True
    global hbond_data_generator
    sample = pyrosetta.rosetta.protocols.data_generation.hbond_machine_learning.Sample
    hbond_data_generator.fill_out_input_values( sample, residue1, residue2 )

    input = numpy.empty( [ 1, 9 ], dtype=float )
    input[ 0 ][ 0 ] = data.Tx
    input[ 0 ][ 1 ] = data.Ty
    input[ 0 ][ 2 ] = data.Tz
    input[ 0 ][ 3 ] = data.Rx
    input[ 0 ][ 4 ] = data.Ry
    input[ 0 ][ 5 ] = data.Rz
    input[ 0 ][ 6 ] = data.Theta1
    input[ 0 ][ 7 ] = data.Theta2
    input[ 0 ][ 8 ] = data.D

    normalize_single_input( input[ 0 ] )

    return input

def evaluate( key, tensor ):
    global all_models
    if not key in all_models:
        return " "
    model = all_models[ key ]
    predictions = model.predict( x=tensor )
    if not len( predictions ) == 1:
        print( "Error: not len( predictions ) == 1" )
        exit( 1 )
    if not len( predictions[ 0 ] ) == 1:
        print( "Error: not len( predictions[ 0 ] ) == 1" )
        exit( 1 )
    if predictions[ 0 ][ 0 ] > 0.5:
        return "1"
    else:
        return "0"

def print_table( pose, task, resid1, resid2 ):
    DEBUG = True
    print( "Table for resids " + str( resid1 ) + " and " + str( resid2 ) )

    res1 = pose.residue( resid1 )
    res2 = pose.residue( resid2 )
    forward_tensor = 0
    reverse_tensor = 0

    all_polar_amino_acids = "DEHKNQRSTQY"
    x_axis_label = ""
    for j in range( 0, len(all_polar_amino_acids) ):
        x_axis_label += str( all_polar_amino_acids[ j ] ) + " "
    #print( x_axis_label )
    out = x_axis_label + "\n"

    for i in range( 0, len(all_polar_amino_acids) ):
        i = all_polar_amino_acids[ i ]
        out_string = str( i )
        for j in range( 0, len(all_polar_amino_acids) ):
            j = all_polar_amino_acids[ j ]
            key = str( i ) + "_" + str( j )
            if i < j:
                if DEBUG:
                    print( "DEBUG: " + i + " and " + j + " use the forward tensor with key: " + key )
                out_string += " " + str( evaluate( key, forward_tensor ) )
            else:
                if DEBUG:
                    print( "DEBUG: " + i + " and " + j + " use the reverse tensor with key: " + key )
                out_string += " " + str( evaluate( key, reverse_tensor ) )
        out += "\n" + out_string
        #print ( out_string )
    print( out )
            

#RUN!
pose = pose_from_pdb( "../3U3B_A.pdb" )
task = standard_packer_task( pose )
for resid in range( 1, pose.size() + 1 ):
    task.nonconst_residue_task( resid ).prevent_repacking()
parse_resfile( pose, task, "small_resfile" )

for resid1 in range( 1, pose.size() + 1 ):
    if not task.being_designed( resid1 ):
        continue
    for resid2 in range( resid1 + 1, pose.size() + 1 ):
        if not task.being_designed( resid2 ):
            continue
        print_table( pose, task, resid1, resid2 )

'''
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

    #input_cache_filename = replace_last_instance_of_substring( input_cache_filename, "/", "/_" )
    #hbond_cache_filename = replace_last_instance_of_substring( hbond_cache_filename, "/", "/_" )

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

ppv=num_positives_actual_and_predicted/num_positives_actual
npv=num_negatives_actual_and_predicted/num_negatives_actual

min_score = ppv
if npv < ppv:
    min_score = npv

print( str(num_positives_actual_and_predicted) + " " +
       str(num_positives_actual) + " " +
       str(ppv) + " " +
       str(num_negatives_actual_and_predicted) + " " +
       str(num_negatives_actual) + " " +
       str(npv) + " " +
       str(min_score)
)
'''
