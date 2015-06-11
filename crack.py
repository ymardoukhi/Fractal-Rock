import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt2d

###----------------------------------Function definitions----------------------------------###

### Cellular Automaton function definition
def cell_auto(array, run_num):
	for n in range(0,run_num):
		print n
		x_size, y_size = np.shape(array)
		new_array = np.zeros((x_size, y_size))
		for i in range(1, x_size-1):
			for j in range(1, y_size-1):
				sum = array[i+1,j] + array[i,j+1] + array[i-1,j] + array[i,j-1] + \
					array[i+1,j+1] + array[i+1,j-1] + array[i-1,j+1] + array[i-1,j-1]
				#print "Sum = %d; Run= %d" %(sum, n)
				if array[i,j] == 0:
					if sum > 4:
						new_array[i,j] = 1
				else:
					if sum < 4:
						new_array[i,j] = 0
					else:
						new_array[i,j] = 1
				sum = 0;
		array = new_array
	return array
### End of Cellular Automaton function definition
###-------------------------------End of Function definitions------------------------------###
		
###-------------------------------------Main Code------------------------------------------###
Y = plt.imread('D:\Dropbox\Fractal Stuties of Rocks\BalmoralRed\JPEG\BR1.jpg')
X = Y[665:1616,1490:2784]
																#Read the input file
X_R = X[:,:,0]													#Red-band image
X_B = X[:,:,1]													#Blue-band image
X_G = X[:,:,2]													#Green-band image

x_size, y_size = np.shape(X_R)									#Getting the shape (size) of the array
CRACK_BOARD_R = np.zeros((x_size, y_size))						#Generating an empty board for red-band image
CRACK_BOARD_B = np.zeros((x_size, y_size))						#Generating an empty board for blue-band image
CRACK_BOARD_G = np.zeros((x_size, y_size))						#Generating an empty board for green-band image

filt_X_R = medfilt2d(X_R)										#Applying the median filter on red-band image
filt_X_B = medfilt2d(X_B)										#Applying the median filter on blue-band image
filt_X_G = medfilt2d(X_G)										#Applying the median filter on green-band image
epsilon = 5														#Setting the threshold for distinguishing the intensitiy change between the cracks boundary

for i in range(1,x_size-1):										#A nested for-loop for finding the initial state of the cells in cellular automata
	for j in range(1,y_size-1):									#The rules are defined in the if statements which can be modified
		if abs(int(filt_X_R[i,j])-int(filt_X_R[i+1,j])) > epsilon or abs(int(filt_X_R[i,j])-int(filt_X_R[i-1,j])) > epsilon or \
		abs(int(filt_X_R[i,j])-int(filt_X_R[i,j+1])) > epsilon or abs(int(filt_X_R[i,j])-int(filt_X_R[i,j-1])) > epsilon or \
		abs(int(filt_X_R[i,j])-int(filt_X_R[i+1,j+1])) > epsilon or abs(int(filt_X_R[i,j])-int(filt_X_R[i+1,j-1])) > epsilon or \
		abs(int(filt_X_R[i,j])-int(filt_X_R[i-1,j+1])) > epsilon or abs(int(filt_X_R[i,j])-int(filt_X_R[i-1,j-1])) > epsilon:
			CRACK_BOARD_R[i,j] = 1
		
		if abs(int(filt_X_B[i,j])-int(filt_X_B[i+1,j])) > epsilon or abs(int(filt_X_B[i,j])-int(filt_X_B[i-1,j])) > epsilon or \
		abs(int(filt_X_B[i,j])-int(filt_X_B[i,j+1])) > epsilon or abs(int(filt_X_B[i,j])-int(filt_X_B[i,j-1])) > epsilon or \
		abs(int(filt_X_B[i,j])-int(filt_X_B[i+1,j+1])) > epsilon or abs(int(filt_X_B[i,j])-int(filt_X_B[i+1,j-1])) > epsilon or \
		abs(int(filt_X_B[i,j])-int(filt_X_B[i-1,j+1])) > epsilon or abs(int(filt_X_B[i,j])-int(filt_X_B[i-1,j-1])) > epsilon:
			CRACK_BOARD_B[i,j] = 1
			
		if abs(int(filt_X_G[i,j])-int(filt_X_G[i+1,j])) > epsilon or abs(int(filt_X_G[i,j])-int(filt_X_G[i-1,j])) > epsilon or \
		abs(int(filt_X_G[i,j])-int(filt_X_G[i,j+1])) > epsilon or abs(int(filt_X_G[i,j])-int(filt_X_G[i,j-1])) > epsilon or \
		abs(int(filt_X_G[i,j])-int(filt_X_G[i+1,j+1])) > epsilon or abs(int(filt_X_G[i,j])-int(filt_X_G[i+1,j-1])) > epsilon or \
		abs(int(filt_X_G[i,j])-int(filt_X_G[i-1,j+1])) > epsilon or abs(int(filt_X_G[i,j])-int(filt_X_G[i-1,j-1])) > epsilon:
			CRACK_BOARD_G[i,j] = 1
		
NEW_CRACK_BOARD_R = cell_auto(CRACK_BOARD_R,30)					#Run the cellular automata for 30 iterations for red-band board array
NEW_CRACK_BOARD_B = cell_auto(CRACK_BOARD_B,30)					#Run the cellular automata for 30 iterations for blue-band board array
NEW_CRACK_BOARD_G = cell_auto(CRACK_BOARD_G,30)					#Run the cellular automata for 30 iterations for green-band board array

Y = np.zeros((x_size,y_size))									#Defining an empty 2D array for averaging purpose
Y = NEW_CRACK_BOARD_R + NEW_CRACK_BOARD_B + NEW_CRACK_BOARD_G	#Summing the state of the three bands (RGB) and average over them
Y = Y/3