import matplotlib.pyplot as plt
import numpy as np


class myPloty:
 def __init__(self,xpos = [], ypos = []):
  xpoints = np.array(xpos)
  ypoints = np.array(ypos)
  self.plot(xpoints,ypoints)

 def plot(self,x,y):
  plt.xlabel("File Size (kB)")
  plt.ylabel("Time (S)") 
  plt.grid()
  plt.plot(x, y)
  plt.show()

py_list = [0.05, 0.09, 5.1, 5.3]
g1 = myPloty(py_list,py_list)
