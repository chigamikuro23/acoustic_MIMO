import math

import numpy as np
import matplotlib 

class Coord:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "({:.1f},{:.1f})".format(self.x,self.y)

  def __repr__(self):
    return str(self)

  def __hash__(self):
      return hash((self.x, self.y))

  def __eq__(self, another):
      return hash(self) == hash(another)

  def l2distance(self, another):
    return math.sqrt((self.x-another.x)**2 + (self.y-another.y)**2)