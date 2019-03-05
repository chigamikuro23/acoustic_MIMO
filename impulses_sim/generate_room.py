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



  
def gen_ref(tx, wall_type, wall_pos):
  distance = 0
  if wall_type == "top" or wall_type == "bottom":
    distance = wall_pos - tx.y
   # print(distance)
    return Coord(tx.x, tx.y+2*distance), wall_type
  else:
    distance = wall_pos - tx.x
  #  print(distance)
    return Coord(tx.x + 2*distance, tx.y), wall_type



def create_room(tx, walls, width, height, counter, max_num, ref_list, seen):
  if counter < max_num:
    seen.add(tx)
  refs = []
  types = []
  new_walls = None
  #print(counter)
  for wall_type, wall_pos in walls.items():
    ref,type_wall = gen_ref(tx, wall_type, wall_pos)
    if ref not in seen:
      refs.append(ref)
      types.append(type_wall)
  ref_list.append(refs)

  if counter < max_num:
    for ref_tx, wall_type in zip(refs,types):
      if wall_type == 'top':
        new_walls = {'top': walls['top']+height, 'right': walls['right'], 'bottom': walls['top'], 'left': walls['left']}
      elif wall_type == 'right':
        new_walls = {'top': walls['top'], 'right': walls['right']+width, 'bottom': walls['bottom'], 'left':walls['right']}
      elif wall_type == 'bottom':
       
        new_walls = {'top': walls['bottom'], 'right': walls['right'], 'bottom': walls['bottom']-height, 'left':walls['left']}
      else:
        
        new_walls = {'top': walls['top'], 'right': walls['left'], 'bottom': walls['bottom'], 'left': walls['left']-width}
      create_room(ref_tx, new_walls, width, height, counter+1, max_num, ref_list, seen)
  else:
  #  print(seen)
    return refs

def get_distances(tx_locations, rx, distances):
  for tx in tx_locations:
    print(tx)
    if not isinstance(tx, (list,)):
      distance = tx.l2distance(rx)
      distances.append([tx, distance])
    else:
      get_distances(tx, rx, distances)
  
  return

walls = {'top': 5, 'right': 10, 'bottom': -5, 'left':-10}
tx = Coord(-3, -1)
counter = 0
max_num = 2
tx_list= []
ref_list = []
seen = set()
create_room(tx, walls, 20, 10, 0, 1, ref_list, seen)
room = [tx]
room.append(ref_list)
print(room)
rx = Coord(5,4)
distances = []
get_distances(room, rx, distances)
print(distances)



#my_set = set([tx, Coord(4,5), Coord(2,3)])
#test = Coord(4,6)
#print(my_set)
#print(test in my_set)



