#!/usr/bin/python

from matplotlib import pylab
import numpy as np
import sys

class visualiser:

    def __init__(self):
        self.count = 0
    
    def set_axis(self,xlo,xhi,ylo,yhi):
        self.xlo = xlo
        self.xhi = xhi
        self.ylo = ylo
        self.yhi = yhi
        
    def set_data(self, data_list):
        self.data = np.array(data_list) #hist requires a numpy.ndarray

    def set_title(self,title):
        self.title = title

    def draw(self):
        
        #data = pylab.randn(500)
        pylab.figure()
        pylab.subplot(111)
        (n,bins,patches) = pylab.hist(self.data,255)
        pylab.title(self.title)
        
        xlo = 0
        xhi = max(abs(bins))
        ylo = 0
        yhi = max(abs(n)) * 1.1
        
        pylab.axis([xlo,xhi,ylo,yhi])
        #pylab.show()
        self.count = self.count + 1
        pylab.savefig("./image_{0}.svg".format(self.count),format="svg")
        print "saved image {0}...".format(self.count)
        pylab.close()
        

    def hist_outline( data_in, *args, **kwargs):
         (hist_in, bins_in) = np.histogram(data_in, *args, **kwargs)

         step_size = bins_in[1] - bins_in[0]

         bins = np.zeros(len(bins_in)*2 + 2, dtype=np.float)
         data = np.zeros(len(bins_in)*2 + 2, dtype=np.float)
         
         for bb in range(len(bins_in)):
             bins[2*bb + 1] = bins_in[bb]
             data[2*bb + 2] = bins_in[bb] + step_size
             
             if bb < len(hist_in):
                 data[2*bb + 1] = hist_in[bb]
                 data[2*bb + 2] = hist_in[bb]
                 
         bins[0] = bins[1]
         bins[-1] = bins[-2]
         data[0] = 0
         data[-1] = 0
                 
         return (bins,data)
