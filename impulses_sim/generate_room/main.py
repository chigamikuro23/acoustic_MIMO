import math
import numpy as np
import matplotlib.pyplot as plt
from room import Room
from coord import Coord


def main():

  walls = {'top': 5, 'right': 10, 'bottom': -5, 'left':-10}

  tx = Coord(1, 1)
  receivers = [Coord(3,4), Coord(4,2)]

  new_room = Room(walls,2)
  new_room.add_transmitter(tx)
  new_room.add_receiver(receivers)
  new_room.create_room()
  attenuations, delays = new_room.get_attenuations_at_index(0)
  delays = np.round(delays).astype(int)
  print(delays)
  plot_arr = np.zeros(np.amax(delays))
  
  h = attenuations*np.exp(-1j*2*np.pi*delays)
  for i in range(len(delays)):
    print(h[i])
    plot_arr[(delays[i]-1)] = np.real(h[i]) 

  plt.stem(plot_arr)
  plt.ylabel('Impulse response')
  plt.xlabel('Time')
  plt.show()






if __name__=="__main__":
  main()

