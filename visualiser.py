#!/usr/bin/python

from matplotlib import pylab
import numpy as np
import sys
import weakref
from scipy import stats
from math import log,sqrt
import cv

class multi_visualiser:

    def __init__(self,n,vis_type):
        assert(n > 0)
        self.count = 0
        self.visualiser = []
        for i in range(n):
            self.visualiser.append(vis_type())


    def set_axis(self,vals):
        assert(len(vals) == len(self.visualiser))
        for i in range(len(vals)):
            self.visualiser[i].set_axis(vals[i])

    def set_nobins(self,no_bins):
        assert(len(no_bins) == len(self.visualiser))

        for i in range(len(no_bins)):
            self.visualiser[i].set_bins(no_bins[i])

    def set_data(self,data_sets):
        assert(len(data_sets) == len(self.visualiser))

        for i in range(len(data_sets)):
            self.visualiser[i].set_data(data_sets[i])

    def set_title(self,titles):
        assert(len(titles) == len(self.visualiser))

        for i in range(len(titles)):
            self.visualiser[i].set_title(titles[i])
            
    def set_ranges(self,vals_ranges):
        assert(len(vals_ranges) == len(self.visualiser))

        for i in range(len(vals_ranges)):
            self.visualiser[i].set_range(vals_ranges[i])

    def draw(self, rows=1,cols=1):
        assert((rows * cols) >= len(self.visualiser))

        fig = pylab.figure() # create the plotting window
        val = (100 * rows) + (10 * cols) + 1 # set index for plotting window
        ax = []
        n = [0] * 2

        for i in range(len(self.visualiser)):
            
            #construct a weak ref to the visualiser instance
            _vis_ref_ = weakref.ref(self.visualiser[i])
            vis_ref = _vis_ref_()
            
            val += i
            ax.append(fig.add_subplot(val))

            (n[i],bins,patches) = ax[i].hist(vis_ref.data, vis_ref.no_bins, normed=True)
            ax[i].set_title(vis_ref.title)
            
            xlo = min(bins)
            xhi = max(bins)
            ylo = 0
            yhi = max(abs(n[i])) * 1.1
        
            ax[i].set_xlim(xlo,xhi)
            ax[i].set_ylim(ylo,yhi)

        #KLA2B = kl_divergence(n[1],n[0])
        #KLA2B_sym = symm_kl_divergence(n[1],n[0])

        #KLB2A = kl_divergence(n[0],n[1])

        #ax[0].set_xlabel("KL = {0}".format(KLA2B))
        #x[1].set_xlabel("KL = {0}".format(KLB2A))
        #ax[0].set_xlabel("CHI2 = {0}".format(chi_squared2(n[1],n[0])))
        ax[0].set_xlabel("bhattacharyya = {0}".format(bhattacharyya_dist(n[1],n[0])))
        #ax[0].set_xlabel("correlation = {0}".format(correlation(n[1],n[0])))
        #ax[1].set_xlabel("CHI2 = {0}".format(chi_squared2(n[0],n[1])))
        #ax[1].set_xlabel("bhattacharyya = {0}".format(bhattacharyya_dist(n[0],n[1])))
        ax[1].set_xlabel("correlation = {0}".format(correlation(n[0],n[1])))


        self.count = self.count + 1
        fig.savefig("./image_{0}.svg".format(self.count),format="svg")
        print "saved image {0}...".format(self.count)    

        ax = fig.add_subplot(val)
        

    def draw_cv(self):

        for i in range(len(self.visualiser)):
             #construct a weak ref to the visualiser instance
            _vis_ref_ = weakref.ref(self.visualiser[i])
            vis_ref = _vis_ref_()

            hist = cv.CreateHist([vis_ref.no_bins],cv.CV_HIST_ARRAY,[vis_ref.get_range()],1)
            
            cv.CalcHist( [vis_ref.data], hist )

            ( _, max_value, _, _) = cv.GetMinMaxHistValue(hist)
            
            hist_img = cv.CreateImage((vis_ref.no_bins,max_value/10),8,3)

            for h in range(vis_ref.no_bins):
                bin_val = cv.QueryHistValue_1D(hist,h)
                cv.Rectangle(hist_img,
                             ((h+1),bin_val/10),
                             (h,0),
                             cv.RGB(255,255,0),
                             cv.CV_FILLED)

            
            cv.NamedWindow("blah",1)
            cv.ShowImage("blah",hist_img)
            cv.WaitKey(0)


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

    def set_bins(self,no_bins):
        self.no_bins = no_bins

    def set_range(self,vals_range):
        self.xlo = vals_range[0]
        self.xhi = vals_range[1]
                                                                   
    def get_range(self):
        return [self.xlo,self.xhi]

    def draw(self):
        
        fig = pylab.figure()
        ax = fig.add_subplot(111)

        (n,bins,patches) = ax.hist(self.data,self.no_bins)
        ax.set_title(self.title)

        #xlo = self.xlo
        #xhi = self.xhi #max(abs(bins))
        xlo = min(bins)
        xhi = max(bins)
        ylo = 0
        yhi = max(abs(n)) * 1.1
        
        ax.set_xlim(xlo,xhi)
        ax.set_ylim(ylo,yhi)

        self.count = self.count + 1
        fig.savefig("./image_{0}.svg".format(self.count),format="svg")
        print "saved image {0}...".format(self.count)
        #pylab.show()
        #fig.close()
        

#comparing B to A
def kl_divergence(distA, distB):
    
    kl_div = 0
    assert(len(distA) == len(distB))
    for i in range(len(distA)):
        if distA[i] == 0 and distB[i] == 0: 
            continue
        if distA[i] <= 0 and  distB[i] >= 0:
            return "undefined"
        kl_div += distB[i] * log( float(distB[i])/distA[i] )

    return kl_div
        
def symm_kl_divergence(distA,distB):
    kl_div = 0
    assert(len(distA) == len(distB))
    for i in range(len(distA)):
        if distA[i] == 0 and distB[i] == 0: 
            continue
        kl_div += (distB[i] - distA[i]) * log( float(distB[i])/distA[i] )

    return kl_div
            
#comparing B to A
def chi_squared(distA, distB):
    
    chi2 = 0
    assert(len(distA) == len(distB))

    for i in range(len(distA)):
        if distA[i] == 0:
            continue

        chi2 += float(distB[i] - distA[i])*(distB[i] - distA[i])/distA[i]

    return chi2

def chi_squared2(distA,distB):

    chi2 = 0
    assert(len(distA) == len(distB))

    for i in range(len(distA)):
        
        chi2 += float(distB[i] - distA[i])*(distB[i] - distA[i])/(distA[i] + distB)

    return chi2
    
    
def correlation(distA,distB):
    
    A_hat = float(sum(distA))/len(distA)
    B_hat = float(sum(distB))/len(distB)
    
    a1 = 0.0
    b1 = 0.0
    b2 = 0.0

    for i in range(len(distA)):

        a_min_mean = distA[i] - A_hat
        b_min_mean = distB[i] - B_hat
        a1 += a_min_mean*b_min_mean
        b1 += a_min_mean*a_min_mean
        b2 += b_min_mean*b_min_mean

    return a1/sqrt(b1*b2)
        

def bhattacharyya_dist(distA,distB):
    
    A_hat = float(sum(distA))
    B_hat = float(sum(distB))

    v = 0
    for i in range(len(distA)):
        v+=sqrt(distA[i]*distB[i])

    return sqrt( 1 - (1.0/sqrt(A_hat*B_hat)) * v)

class cv_visualiser(visualiser):

    
      def set_data(self, data_list):
          self.data = cv.CreateImage((1,len(data_list)),cv.IPL_DEPTH_32F,1)
          for i in range(len(data_list)):
              self.data[i,0] = data_list[i]
          #cv.SetData(self.data,data_list,cv.CV_AUTOSTEP)
          assert(self.data[0,0] == data_list[0])
