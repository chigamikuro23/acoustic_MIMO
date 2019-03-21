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

    tx = Coord(5,5)
    receivers = [Coord(3,4), Coord(5,6), Coord(5,5)]

    index = 1
    amplitude = 1

    new_room = Room(walls,4)

    SNR_dB = 2

    new_room.add_transmitter(tx)
    new_room.add_receiver(receivers)
    new_room.create_room()


  

    new_room.calculate_h(amplitude, index)

    #Add standard white gaussian noise
    upsample_factor = 10
    filter_type = 'sinc'
    

    new_room.pulse_shape(filter_type, upsample_factor)
   
    new_room.add_gaussian_noise(SNR_dB)
    print(new_room)

    new_room.plot_h_at_index(index)
    new_room.plot_fft(filter_type, upsample_factor)

    plt.show()

    
    





if __name__=="__main__":
  main()

