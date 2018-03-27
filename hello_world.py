#from keras import *
from keras.models import Sequential
from keras.layers import Dense
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
#PAIR = int( 8 )
#CENPACK = int( 9 )
ANGLE1 = int( 10 )
ANGLE2 = int( 11 )
DIST   = int( 12 )

dataset = numpy.genfromtxt( "sample_data.csv", delimiter=",", skip_header=1 )
print( len( dataset[ 0 ] ) )

input = dataset[:,[ TX, TY, TZ, RX, RY, RZ, ANGLE1, ANGLE2, DIST ] ]
output = dataset[:,0:2]
