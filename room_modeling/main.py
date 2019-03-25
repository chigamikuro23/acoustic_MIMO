import math

from room import Room
from coord import Coord
import numpy as np
import matplotlib.pyplot as plt
import sys

def main():

  if len(sys.argv) == 2 and sys.argv[1] == "-custom":
    print("Custom")

  else:

    print("Default")

	
    walls = {'top': 10, 'right': 10, 'bottom': -10, 'left':-10}


    transmitters = [Coord(4,4), Coord(3,7), Coord(-9,3), Coord(-3,2), Coord(-5, -4), Coord(4,-7), Coord(6,-9), Coord(-4,-1), Coord(-9,-9), Coord(2,8)]
    receivers = [Coord(3,4), Coord(5,6)]
    tx_index = 0
    rx_index = 1
    amplitude = 1

    new_room = Room(walls,10)

    
    new_room.add_transmitter(transmitters)
    new_room.add_receiver(receivers)
    upsample_factor = 10
    filter_type = 'sinc'

    for tx_index, tx_value in enumerate(transmitters):
        for rx_index, rx_value in enumerate(receivers):
            new_room.create_room(tx_index)
            new_room.calculate_h(tx_index, rx_index)
            new_room.pulse_shape(filter_type, upsample_factor)
          #  new_room.plot_h_at_index(tx_index, rx_index)
            new_room.plot_fft(filter_type, upsample_factor)
         #   new_room.write_to_wav(f"impulses/impulses_{tx_value}_{rx_value}.wav")

    #Add standard white gaussian noise
 
    
    #SNR_dB = 2
   # new_room.add_gaussian_noise(SNR_dB)
   # print(new_room)

   # new_room.plot_h_at_index(tx_index, rx_index, SNR_dB)
  #  new_room.plot_fft(filter_type, upsample_factor)
  #  new_room.write_to_wav("impulses_with_noise.wav")

    #new_room.read_wav_and_plot("impulses_with_noise.wav")
    plt.show()

    
    





if __name__=="__main__":
  main()

