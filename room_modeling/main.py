import math

from room import Room
from coord import Coord
import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.io as sio

def main():

	if len(sys.argv) == 2 and sys.argv[1] == "-custom":
		print("Custom")

	else:

		print("Default")

		
		walls = {'top': 10, 'right': 10, 'bottom': -10, 'left':-10}


   # transmitters = [Coord(4,4), Coord(3,7), Coord(-9,3), Coord(-3,2), Coord(-5, -4), Coord(4,-7), Coord(6,-9), Coord(-4,-1), Coord(-9,-9), Coord(2,8),
   # Coord(1,1), Coord(8,9), Coord(-9,-2), Coord(-6,-5), Coord(-8, -9), Coord(2,-3), Coord(0,-4), Coord(-2,-2), Coord(-8,-2), Coord(7,2)]
   # transmitters = [Coord(-9.0,-9.0)]

	  
		receivers = [Coord(3.0,4.0), Coord(-3.0, -4.0)]
		tx_index = 0
		rx_index = 1
		amplitude = 1

		new_room = Room(walls,1)
		margin = .5
		width = new_room.width - margin 
		height = new_room.height - margin

		transmitters = []

		num_rows = 40
		num_cols = 40
		x_start = new_room.walls['left'] +.25
		y_start = new_room.walls['bottom'] +.25 

		x_delta = width/num_cols
		y_delta = height/num_rows

		indices = []
		index = 0.0
		for i in range(num_rows):
			for j in range(num_cols):
				x = x_start + i*x_delta
				y = y_start + j*y_delta
				transmitters.append(Coord(x,y))
				indices.append(index)
				index +=1.0


		#print(transmitters)

	    
		new_room.add_transmitter(transmitters)
		new_room.add_receiver(receivers)
		upsample_factor = 10
		filter_type = 'sinc'

		input_signal = None
		positions = []
		real = []
		imag = []
		num_time_samples = 10
		t = -1
		h = None
		for tx_index, tx_value in enumerate(transmitters):
			temp_real = []
			temp_imag = []
			for rx_index, rx_value in enumerate(receivers):
				new_room.create_room(tx_index)
				new_room.calculate_h(tx_index, rx_index)
				if (rx_value.l2distance(tx_value) <=1):
					
					new_room.convolve_input(tx_value, rx_value, "speech.wav")
				else:
					new_room.pulse_shape(filter_type, upsample_factor)
				if (t == -1): 
					t = np.argmax(new_room.h>0)
					print(t)
				
	    			

				value = np.sum(new_room.h[t:t+num_time_samples])/num_time_samples

		#new_room.plot_h_at_index(tx_index, rx_index)
		# new_room.plot_fft(filter_type, upsample_factor)
		# new_room.write_to_wav(f"impulses/impulses_{tx_value}_{rx_value}.wav")
				temp_real.append(np.real(value))
				temp_imag.append(np.imag(value)) 
			real.append(temp_real)
			imag.append(temp_imag)
			positions.append([tx_value.x, tx_value.y])
	    
	   # print(input_fs)

	   fs, data = wavfile.read(filename)



	   # new_room.plot_h_at_index(tx_index, rx_index, SNR_dB)
	  #  new_room.plot_fft(filter_type, upsample_factor)
	  #  new_room.write_to_wav("impulses_with_noise.wav")

	   # new_room.convolve_input("speech.wav")
	  #  plt.show()
		real = np.array(real)
		imag = np.array(imag)
		print(positions)
		num_ant = len(receivers)
		num_samples = num_rows * num_cols

		print(real.shape)
		print(imag.shape)
		h_coeff_real = np.hstack((real, imag))


		mat_contents = { "h_coeff_real":h_coeff_real.transpose(), "index":indices, "num_ant":num_ant, "num_samples":num_samples, "positions":np.array(positions).transpose()}
		sio.savemat("impulses.mat", mat_contents)

		#print(mat_contents)
		plt.show()

if __name__=="__main__":
  main()

