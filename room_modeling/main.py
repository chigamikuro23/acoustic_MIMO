import math

from room import Room
from coord import Coord
import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.io as sio
import h5py
import hdf5storage


def main():

	if len(sys.argv) == 2 and sys.argv[1] == "one":
		walls = {'top': 50, 'right': 50, 'bottom': -50, 'left':-50}


		transmitters = [Coord(-30.0, -1.0)]
		receivers = [Coord(-49.0, -1.0)]

		new_room = Room(walls,2)
		margin = .5
		width = new_room.width - margin 
		height = new_room.height - margin

		new_room.add_transmitter(transmitters)
		new_room.add_receiver(receivers)

		filter_type = 'sinc'

		SNR_dB = 10
		new_room.create_room(0)
		new_room.calculate_h(0, 0)

		new_room.pulse_shape(filter_type)
		#new_room.add_channel_noise(SNR_dB)


		new_room.plot_h_at_index(transmitters[0], receivers[0], new_room.fs_upsampled)

		freq, fft = new_room.get_fft(filter_type)

		plt.plot(freq, np.abs(fft))

		plt.title(f"FFT with sampling freq {new_room.fs_upsampled}; Filter type: {filter_type}")
		plt.ylabel('FFT Magnitude')
		plt.xlabel('Freq (Hz)')

		plt.show()

	elif len(sys.argv) == 2 and sys.argv[1] == "complete":
		print("Full impulse")
		
		walls = {'top': 50, 'right': 50, 'bottom': -50, 'left':-50}


   # transmitters = [Coord(4,4), Coord(3,7), Coord(-9,3), Coord(-3,2), Coord(-5, -4), Coord(4,-7), Coord(6,-9), Coord(-4,-1), Coord(-9,-9), Coord(2,8),
   # Coord(1,1), Coord(8,9), Coord(-9,-2), Coord(-6,-5), Coord(-8, -9), Coord(2,-3), Coord(0,-4), Coord(-2,-2), Coord(-8,-2), Coord(7,2)]
   # transmitters = [Coord(-9.0,-9.0)]
		num_ant = 16
		receivers = []
		rx_delta = .10
		y_start = -1.0
		for i in range(num_ant):
			y = y_start + i*rx_delta
			receivers.append(Coord(-49.90,y))

		print(receivers)
		#receivers = [Coord(3.0,4.0), Coord(-3.0, -4.0)]

		tx_index = 0
		rx_index = 1
		amplitude = 1

		new_room = Room(walls,2)
		margin = .5
		width = new_room.width - margin 
		height = new_room.height - margin

		transmitters = []

		num_rows =40
		num_cols = 40
		x_start = new_room.walls['left'] +.25
		y_start = new_room.walls['bottom'] +.25 

		x_delta = width/num_cols
		y_delta = height/num_rows

		for i in range(num_rows):
			for j in range(num_cols):
				x = x_start + i*x_delta
				y = y_start + j*y_delta
				transmitters.append(Coord(x,y))
		


		#print(transmitters)

	    
		new_room.add_transmitter(transmitters)
		new_room.add_receiver(receivers)

		filter_type = 'sinc'

		input_signal = None

		h = None
		impulses = []
		count = 0
		for tx_index, tx_value in enumerate(transmitters):


			for rx_index, rx_value in enumerate(receivers):
				new_room.create_room(tx_index)
				new_room.calculate_h(tx_index, rx_index)
			#	if (rx_value.l2distance(tx_value) <=1):
				new_room.pulse_shape(filter_type)
				impulses.append(np.real(new_room.h))
			

				
	    			

				

		#new_room.plot_h_at_index(tx_index, rx_index)
		# new_room.plot_fft(filter_type, upsample_factor)
		# new_room.write_to_wav(f"impulses/impulses_{tx_value}_{rx_value}.wav")

			
	    
	   # print(input_fs)

	  # fs, data = wavfile.read(filename)


		#new_room.plot_h_at_index(tx_index, rx_index, SNR_dB)
		#new_room.plot_fft(filter_type)
	  #  new_room.write_to_wav("impulses_with_noise.wav")

	   # new_room.convolve_input("speech.wav")
	  #  plt.show()


	#	print(positions)
		impulses = np.vstack(impulses)
		print(impulses)
		num_samples = num_rows * num_cols

		#print(real.shape)
		#print(imag.shape)
	
		par = {"sampling_freq": new_room.fs_upsampled, "upsample_factor":new_room.upsample_factor, "max_order": new_room.max_order, "num_samples":num_samples, "num_ant":num_ant, "upsampling_factor":new_room.upsample_factor, "room_width":new_room.width, "room_height":new_room.height, "pulse_shape_fct":filter_type}

		mat_contents = { "impulses":impulses.transpose(), "num_ant":num_ant, "num_samples":num_samples, "par":par}
		print(mat_contents)
		#sio.savemat("impulses_complete.mat", mat_contents)
		hdf5storage.write(mat_contents, '.', 'impulses_complete.mat', matlab_compatible=True)
		#print(mat_contents)
		new_room.plot_h_at_index(tx_value, rx_value, new_room.fs_upsampled)
		new_room.plot_fft(filter_type)
		plt.show()


	elif len(sys.argv) == 2 and sys.argv[1] == "csi":

		print("Channel State Information")

		
		walls = {'top': 50, 'right': 50, 'bottom': -50, 'left':-50}


   # transmitters = [Coord(4,4), Coord(3,7), Coord(-9,3), Coord(-3,2), Coord(-5, -4), Coord(4,-7), Coord(6,-9), Coord(-4,-1), Coord(-9,-9), Coord(2,8),
   # Coord(1,1), Coord(8,9), Coord(-9,-2), Coord(-6,-5), Coord(-8, -9), Coord(2,-3), Coord(0,-4), Coord(-2,-2), Coord(-8,-2), Coord(7,2)]
   # transmitters = [Coord(-9.0,-9.0)]
		num_ant = 30
		receivers = []
		rx_delta = .10
		y_start = -1.0
		for i in range(num_ant):
			y = y_start + i*rx_delta
			receivers.append(Coord(-49.90,y))

		print(receivers)
		#receivers = [Coord(3.0,4.0), Coord(-3.0, -4.0)]

		tx_index = 0
		rx_index = 1
		amplitude = 1

		new_room = Room(walls,2)
		margin = .5
		width = new_room.width - margin 
		height = new_room.height - margin

		transmitters = []

		num_rows = 50
		num_cols = 50
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

		filter_type = 'sinc'

		input_signal = None
		positions = []
		real = []
		imag = []
		SNR_dB = 10
		t = -1
		h = None
		within = 0
		center = 0
		for tx_index, tx_value in enumerate(transmitters):
			temp_real = []
			temp_imag = []

			for rx_index, rx_value in enumerate(receivers):
				new_room.create_room(tx_index)
				new_room.calculate_h(tx_index, rx_index)
				
			#	if (rx_value.l2distance(tx_value) <=1):
				#if False:		
				#new_room.convolve_input(tx_value, rx_value, "speech.wav")
			#	else:
				new_room.pulse_shape(filter_type)
				new_room.add_channel_noise(SNR_dB)
				freqs, fft = new_room.get_fft(filter_type)
			#	if (t == -1): 
			#		t = np.argmax(new_room.h)
					
			#		print(t)
				#else:
				#	if abs(np.argmax(new_room.h)-t)<=num_time_samples//2: within +=1

				value = fft[len(freqs)//2+10]
		
			#	value = new_roofm.h[t]
				#value = np.mean(new_room.h[t-num_time_samples//2:t+num_time_samples//2])

		#new_room.plot_h_at_index(tx_index, rx_index)
		# new_room.plot_fft(filter_type, upsample_factor)
		# new_room.write_to_wav(f"impulses/impulses_{tx_value}_{rx_value}.wav")
				temp_real.append(np.real(value))
				temp_imag.append(np.imag(value)) 
			
			real.append(temp_real)
			imag.append(temp_imag)
			positions.append([tx_value.x, tx_value.y])
	    
	   # print(input_fs)

	  # fs, data = wavfile.read(filename)


		#new_room.plot_h_at_index(tx_index, rx_index, SNR_dB)
		#new_room.plot_fft(filter_type)
	  #  new_room.write_to_wav("impulses_with_noise.wav")

	   # new_room.convolve_input("speech.wav")
	  #  plt.show()

		real = np.array(real)
		imag = np.array(imag)
	#	print(positions)
		
		num_samples = num_rows * num_cols
		print(within/(num_samples*num_ant))
		#print(real.shape)
		#print(imag.shape)
		h_coeff_real = np.hstack((real, imag))
		par = {"sampling_freq": new_room.fs_upsampled, "upsample_factor":new_room.upsample_factor, "max_order": new_room.max_order, "num_samples":num_samples, "num_ant":num_ant, "upsampling_factor":new_room.upsample_factor, "room_width":new_room.width, "room_height":new_room.height, "pulse_shape_fct":filter_type, "channel_SNR_dB": SNR_dB}

		mat_contents = { "h_coeff_real":h_coeff_real.transpose(), "index":indices, "num_ant":num_ant, "num_samples":num_samples, "par":par, "positions":np.array(positions).transpose()}
		
		print(mat_contents)
		#sio.savemat("impulses_avg.mat", mat_contents)
		hdf5storage.write(mat_contents, '.', 'impulses_fft_with_noise_44_1_kHz.mat', matlab_compatible=True)
		
		new_room.plot_h_at_index(tx_value, rx_value, new_room.fs_upsampled)

		freq, fft = new_room.get_fft(filter_type)

		plt.plot(freq, np.abs(fft))

		plt.title(f"FFT with sampling freq {new_room.fs_upsampled}; Filter type: {filter_type}")
		plt.ylabel('FFT Magnitude')
		plt.xlabel('Freq (Hz)')

		plt.show()

	else:
		print("Need at least two arguments and a valid command")

if __name__=="__main__":
  main()

