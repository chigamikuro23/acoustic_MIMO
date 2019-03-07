import math
import numpy as np
import matplotlib 

class Coord:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "({},{})".format(self.x,self.y)

  def __repr__(self):
    return str(self)

  def __hash__(self):
      return hash((self.x, self.y))

  def __eq__(self, another):
      return hash(self) == hash(another)

  def l2distance(self, another):
    return math.sqrt((self.x-another.x)**2 + (self.y-another.y)**2)


class Room:

  def __init__(self, walls, max_order=0):
    self.walls = walls
    self.width = abs(walls['left'] - walls['right'])
    self.height = abs(walls['top'] - walls['bottom'])
    self.transmitters = []
    self.receivers = []
    self.distances = []
    self.reflections = []
    self.delays = []
    self.max_order = max_order
    
  
  def __str__(self):

    return "Walls:{}, Width: {}, Height:{}, \n Tx(s): {} \n Rx(s):{} \n Max Order: {},\n Ref: {}\n Distances: {}".format(self.walls, self.width, self.height, self.transmitters, self.receivers, self.max_order,  self.reflections, self.distances)




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
  def create_room(self):
    
    if self.transmitters:
      seen = set()
      room = [self.transmitters[0]]

      if self.max_order > 0:
        self.create_room_rec(self.transmitters[0], self.walls, self.width, self.height, 1, self.reflections, seen)
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

  def plot_reflections_at_index(self, index):

    return


def main():
  #walls = {'top': 5, 'right': 10, 'bottom': -5, 'left':-10}
  walls = {'top': 5, 'right': 10, 'bottom': -5, 'left':0}

  tx = Coord(1, 1)
  receivers = [Coord(3,4), Coord(4,2)]

  new_room = Room(walls,3)
  new_room.add_transmitter(tx)
  new_room.add_receiver(receivers)
  new_room.create_room()
  print(new_room.get_distances_at_index(0))
  return

if __name__=="__main__":
  main()

