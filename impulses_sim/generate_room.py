import math
import numpy as np

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

  def __init__(self, walls):
    self.walls = walls
    self.width = abs(walls['left'] - walls['right'])
    self.height = abs(walls['top'] - walls['bottom'])
    self.transmitters = []
    self.receivers = []
    self.distances = []
    self.reflections = []
    self.max_order = 0
    
  
  def __str__(self):

    return "Walls:{}, Width: {}, Height:{}, \n Tx(s): {} \n Rx(s):{} \n Max Order: {},\n Ref: {}\n Distances: {}".format(self.walls, self.width, self.height, self.transmitters, self.receivers, self.max_order,  self.reflections, self.distances)


  def inBounds(self, location):

    return location.x >= self.walls['left'] and location.x<=self.walls['right'] and location.y <=self.walls['top'] and location.y >=self.walls['bottom'] 

  def add_transmitter(self, tx):
    if isinstance(tx, (list,)): 
      for transmitter in tx:
        if not self.inBounds(transmitter): 
          print("Tx not in walls")
          return
      self.transmitters = tx
    else:
      if not self.inBounds(tx): 
        print("Tx not in walls")
        return
      self.transmitters.append(tx)

  def add_receiver(self, rx):
    if isinstance(rx, (list,)): 
      for receiver in rx:
        if not self.inBounds(receiver): 
          print("Rx not in walls")
          return
      self.receivers = rx
    else:
      if not self.inBounds(rx): 
        print("Rx not in walls")
        return
      self.receivers.append(rx)



  
  def create_room(self, max_order):
    self.max_order = max_order
    if self.transmitters:
      seen = set()
      room = [self.transmitters[0]]

      if max_order > 0:
        self.create_room_rec(self.transmitters[0], self.walls, self.width, self.height, 1, max_order, self.reflections, seen)
        room.append(self.reflections)
      
      self.get_distances(room, self.receivers[0] ,self.distances)



    else:
      return None
    
  def create_room_rec(self, tx, walls, width, height, counter, max_order, ref_list, seen):

    
   

    if counter < max_order:
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

    if counter < max_order:
      for ref_tx, wall_type in zip(refs,types):
        if wall_type == 'top':
          new_walls = {'top': walls['top']+height, 'right': walls['right'], 'bottom': walls['top'], 'left': walls['left']}
        elif wall_type == 'right':
          new_walls = {'top': walls['top'], 'right': walls['right']+width, 'bottom': walls['bottom'], 'left':walls['right']}
        elif wall_type == 'bottom':
        
          new_walls = {'top': walls['bottom'], 'right': walls['right'], 'bottom': walls['bottom']-height, 'left':walls['left']}
        else:
          
          new_walls = {'top': walls['top'], 'right': walls['left'], 'bottom': walls['bottom'], 'left': walls['left']-width}
        self.create_room_rec(ref_tx, new_walls, width, height, counter+1, max_order, ref_list, seen)
    else:
      return refs



    

    
  def gen_ref(self, tx, wall_type, wall_pos):
    distance = 0
    if wall_type == "top" or wall_type == "bottom":
      distance = wall_pos - tx.y
      return Coord(tx.x, tx.y+2*distance), wall_type
    else:
      distance = wall_pos - tx.x
      return Coord(tx.x + 2*distance, tx.y), wall_type




  def get_distances(self, tx_locations, rx, distances):
    for tx in tx_locations:
     # print(tx)
      if not isinstance(tx, (list,)):
        distance = tx.l2distance(rx)
        distances.append((tx, distance))
      else:
        self.get_distances(tx, rx, distances)
        self.distances.sort(key=lambda x: x[1])
    
    return

  def plot_room(self):

    return



'''
att = [(item[0], 1/item[1]) for item in distances]
print(att)

'''
walls = {'top': 5, 'right': 10, 'bottom': -5, 'left':-10}

tx = Coord(-3, -1)
rx = Coord(3,4)



new_room = Room(walls)
new_room.add_transmitter(tx)
new_room.add_receiver(rx)
new_room.create_room(0)
print(new_room)

