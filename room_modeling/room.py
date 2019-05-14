from coord import Coord
from collections import Counter, defaultdict
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn, resample
from scipy.io import wavfile
class Room:

  def __init__(self, walls, max_order=0, upsample_factor = 10, fs = 4410, v = 340):
    self.walls = walls
    self.width = abs(walls['left'] - walls['right'])
    self.height = abs(walls['top'] - walls['bottom'])
    self.transmitters = []
    self.receivers = []
    self.distances = []
    self.reflections = []
    self.delays = []
    self.max_order = max_order
    self.fs = fs
    self.upsample_factor = upsample_factor
    self.fs_upsampled = fs*upsample_factor
    self.v = v
    self.wavelength = v/fs 
    self.h = None
  
  def __str__(self):

    return "Walls:{} \n Width: {}, Height:{} \n Tx(s): {} \n Rx(s):{} \n Max Reflection Order: {}\n Sampling Frequency: {}Hz \n Sound Velocity: {} m/s".format(self.walls, self.width, self.height, self.transmitters, self.receivers, self.max_order, self.fs, self.v)




 #Utility functions that return different attributes of this room
  def get_all_distances(self):
    return self.distances

  def get_distances_at_index(self,index):
    return self.distances[index]

  def get_transmitters(self):
    return self.transmitters

  def get_receivers(self):
    return self.receivers

  def get_max_order(self):
    return self.max_order

 #Checks if a point is within the bounds of the room
  def in_bounds(self, location):
    return location.x >= self.walls['left'] and location.x<=self.walls['right'] and location.y <=self.walls['top'] and location.y >=self.walls['bottom'] 


  #Adds a transmitter or list of transmitters to this room
  def add_transmitter(self, tx):
    if isinstance(tx, (list,)): 
      for transmitter in tx:
        if not self.in_bounds(transmitter): 
          print("Tx not in walls")
          return
      self.transmitters += tx
    else:
      if not self.in_bounds(tx): 
        print("Tx not in walls")
        return
      self.transmitters.append(tx)


  #Adds a receiver or list of receivers to this room
  def add_receiver(self, rx):
    if isinstance(rx, (list,)): 
      for receiver in rx:
        if not self.in_bounds(receiver): 
          print("Rx not in walls")
          return
      self.receivers += rx
    
    else:
      if not self.in_bounds(rx): 
        print("Rx not in walls")
        return
      self.receivers.append(rx)




  #Wrapper function that creates the room reflections based on the transmitter(s) and receiver(s) that are inside this room
  def create_room(self, tx_index):
    if not self.transmitters or not self.receivers:
      raise("Need at least one transmitter and receiver available")

    if self.transmitters:
      self.distances = []
      self.reflections = []
      self.delays = []
      self.h = None
      seen = set()
      room = [self.transmitters[tx_index]]

      if self.max_order > 0:
        self.create_room_rec(self.transmitters[tx_index], self.walls, self.width, self.height, 1, self.reflections, seen)
        room.append(self.reflections)
      
      for receiver in self.receivers:
        distances_unit = []
        self.calculate_distances(room, receiver, distances_unit)
        self.distances.append(distances_unit)
    else:
      return None
    
  #Function that recursively finds the coordinates of image sources based on given transmitter
  def create_room_rec(self, tx, walls, width, height, counter, ref_list, seen):
    if counter < self.max_order:
      seen.add(tx)
    refs = []
    types = []
    new_walls = None
    for wall_type, wall_pos in walls.items():
      ref,type_wall = self.gen_ref(tx, wall_type, wall_pos)
      if ref not in seen:
        refs.append(ref)
        types.append(type_wall)
    ref_list.append(refs)

    if counter < self.max_order:
      for ref_tx, wall_type in zip(refs,types):
        if wall_type == 'top':
          new_walls = {'top': walls['top']+height, 'right': walls['right'], 'bottom': walls['top'], 'left': walls['left']}
        elif wall_type == 'right':
          new_walls = {'top': walls['top'], 'right': walls['right']+width, 'bottom': walls['bottom'], 'left':walls['right']}
        elif wall_type == 'bottom':
        
          new_walls = {'top': walls['bottom'], 'right': walls['right'], 'bottom': walls['bottom']-height, 'left':walls['left']}
        else:
          
          new_walls = {'top': walls['top'], 'right': walls['left'], 'bottom': walls['bottom'], 'left': walls['left']-width}
        self.create_room_rec(ref_tx, new_walls, width, height, counter+1, ref_list, seen)
    else:
      return refs



    

  #Calculates the coordinate of one image source of a transmitter based on wall direction    
  def gen_ref(self, tx, wall_type, wall_pos):
    distance = 0
    if wall_type == "top" or wall_type == "bottom":
      distance = wall_pos - tx.y
      return Coord(tx.x, tx.y+2*distance), wall_type
    else:
      distance = wall_pos - tx.x
      return Coord(tx.x + 2*distance, tx.y), wall_type



  #Calculates each transmitter(original or image)'s' distance from a receiver
  def calculate_distances(self, tx_locations, rx, distances):
    for tx in tx_locations:
     # print(tx)
      if not isinstance(tx, (list,)):
        distance = tx.l2distance(rx)
        distances.append((tx, distance))
      else:
        self.calculate_distances(tx, rx, distances)
        distances.sort(key=lambda x: x[1])
 
    
    return 

  def get_attenuations_at_index(self, index):
    distance_ref = self.distances[index]
    #print(distance_ref)
    attenuations = [1/item[1] for item in distance_ref]
    distances = [item[1] for item in distance_ref]
    counter = -1

    ret_att = []
    delays = []
    seen = set()
  #  print(attenuations)
    for dist, att in zip(distances, attenuations):
      if att not in seen:

        delays.append(dist/self.wavelength)
        seen.add(att)
        ret_att.append(att)
        counter+=1
      else:
        ret_att[counter]+=att
 #   print(ret_att)
 #   print(delays)
    return np.array(ret_att), np.array(delays)

  def calculate_h(self, tx_index, rx_index):
    attenuations, delays = self.get_attenuations_at_index(rx_index)
    delays = np.round(delays).astype(int)
    #print(delays)
    self.h = np.zeros(self.fs, dtype=complex)


    h_list = attenuations*np.exp(-1j*2*np.pi*delays)
    for i in range(len(delays)):
    ##  print(h[i])
      self.h[(delays[i]-1)] = h_list[i] 

 #   print(len(self.h))
    return 
  def plot_h_at_index(self, tx_value, rx_value, freq):

    plt.figure()
    t = np.linspace(0, len(self.h)/freq, len(self.h))
    
    plt.plot(t, np.real(self.h))
    plt.title("Position at {}, Rx at {}, max_order = {}".format(tx_value, rx_value, self.max_order))
    plt.ylabel('Real Amplitude')
    plt.xlabel('Time (s)')

    plt.figure()
    plt.plot(t, np.imag(self.h))
    plt.title("Position at {}, Rx at {}, max_order = {}".format(tx_value, rx_value, self.max_order))
    plt.ylabel('Imaginary Amplitude')
    plt.xlabel('Time (s)')
    return
        


  def get_fft(self, filter_type):
   # plt.figure()

    fft = np.fft.fft(self.h)/np.sqrt(len(self.h))
    freq = np.fft.fftfreq(len(self.h), d=1/self.fs_upsampled)
    
   # plt.plot(freq, np.abs(fft))

   # plt.title(f"FFT with upsample factor {self.upsample_factor}; Filter type: {filter_type}")
   # plt.ylabel('FFT Amplitude')
  #  plt.xlabel('Freq (kHz)')

    return freq, fft



  def pulse_shape(self, filter_type):


   # print(f"Filter type: {filter_type}")
   # print(f"Upsample factor: {factor}")
    factor = self.upsample_factor
   # print(factor)
    upsample_vector = upfirdn([1], self.h, factor)
    
    my_filter = None
    if filter_type == "rectangular":
      my_filter = np.ones(factor)
    else:
     # my_filter =np.sin(np.pi*np.arange(-factor,factor+1/factor,1/factor))/(np.pi*np.arange(-factor,factor+1/factor,1/factor))
      my_filter = np.sinc(np.arange(-factor,factor+1/factor,1/factor))
      
    convolved = np.convolve(upsample_vector, my_filter)
    self.h = convolved[0:self.fs_upsampled]
  
   # print(len(self.h))

    return


  def add_channel_noise(self, SNR_dB):
   # print(f"SNR_dB = {SNR_dB}")
    #print(self.fs_upsampled)
    p_signal = np.mean(np.square(np.absolute(self.h)))
    p_noise = p_signal*(10**(-SNR_dB/10.0))

    noise = np.random.normal(0, np.sqrt(p_noise/2), len(self.h)) + 1j*np.random.normal(0, np.sqrt(p_noise/2), len(self.h))
 #   print(f"Adding gaussian noise with power {p_noise}")
    self.h += noise


    return

 
  def write_to_wav(self, filename):
    wavfile.write(filename, self.fs_upsampled, self.h.astype('f8'))
    return

  def read_wav_and_plot(self, filename):
    fs, data = wavfile.read(filename)
    plt.figure()
    t = np.linspace(0, len(data)/fs, len(data))
    plt.plot(t, np.real(data))

    plt.ylabel('Real Amplitude')
    plt.xlabel('Time')
    return fs, data

  def convolve_input(self, tx_value, rx_value, filename):
    fs, data = wavfile.read(filename)
    self.h = upfirdn([1], self.h, 10)
    other = resample(self.h, fs)

    length = len(data)
    plt.figure()
    plt.plot(data)
    plt.title(f"Input speech, fs={fs}")
    plt.ylabel('Amplitude')
    plt.xlabel('Time index')

    print(data.dtype)
    output = np.convolve(other, data)
    plt.figure()
    plt.plot(output[0:length])
    plt.title(f"Tx:{tx_value}, Rx:{rx_value}, Convolved, max_order = {self.max_order}, fs = {fs}")
    plt.ylabel('Amplitude')
    plt.xlabel('Time index')

    folder_str = "output_speeches/"
    tx_str = str(tx_value).replace(".","_")
    rx_str = str(rx_value).replace(".","_")
    out_filename = folder_str + tx_str + rx_str + "_output.wav" 
    wavfile.write(out_filename, fs, output.astype('int16') )
    return output







