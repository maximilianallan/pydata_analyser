#!/usr/bin/python

import cv,visualiser

class converter:


    def __init__(self, im_stack, mask_stack):

        self.im_stack = im_stack
        self.mask_stack = mask_stack
        self.converters = []
        self.converters.append(converter.rgb2rgb)
        self.converters.append(converter.rgb2hsv)
        self.converters.append(converter.rgb2cie)
        self.converters.append(converter.rgb2sift)

    def parse_images(self):


        for funct in self.converters:
            for image in range(len(self.im_stack)):
                
                self.parse_pair(self.im_stack[image],
                                self.mask_stack[image],
                                funct)
                print "done image"
            print "done function"
                
                
    def parse_pair(self,image,mask,convert):
        
        new_im = convert(image)
        
        #class_pix[n] has size(channels) lists of the pixel vals in the class n
        self.class_pix = [ [[] for i in range(image.nChannels)],
                           [[] for i in range(image.nChannels)] ]
        self.get_pixels(new_im,mask,self.class_pix)
        
             
    def get_pixels(self,image,mask,class_pix):
        
        """
        get_pixels ---> push the pixels into list according to bitmask
        @param image is the image to take the pixels from
        @param mask is the bitmasks which specifies which list to push the pixels to
        @param class pix is a list of nested lists, each index of the list corresponds to a class and and the value associated with than index corresponds a list of channels each containing a list of pixels that have been allocated to that class by the bitmask
        """       
            
        if not cmp(image.width,mask.width):
            return
        if not cmp(image.height,mask.height):
            return


        for r in range(image.height):
            for c in range(image.width):
                pix = image[r,c]
                for n in range(image.nChannels):
                    #push pixels according to mask
                    if cmp(mask[r,c],[255.0,255.0,255.0]):
                        class_pix[0][n].append(pix[n])
                    elif cmp(mask[r,c],[0.0,0.0,0.0]):
                        class_pix[1][n].append(pix[n])
                    else:
                        print "error!"
                            
                            
    @staticmethod
    def rgb2rgb(in_im):
        return in_im;

    @staticmethod
    def rgb2hsv(in_im,out_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                in_im.depth,
                                in_im.nChannels)
        cv2.cvtColor(in_im,out_im,cv.CV_RGB2HSV)
        return out_im


    @staticmethod
    def rgb2cie(in_im,out_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                in_im.depth,
                                in_im.nChannels)
        cv2.cvtColor(in_im,out_im,cv.CV_RGB2XYZ)
        return out_im
    
    @staticmethod
    def rgb2sift(in_im,out_im):
        keypoint = []
        gray = cv.CreateImage(cv.GetSize(in_im),
                              in_im.depth,
                              1)
        """
        for r in range(in_im.height):
        for c in range(in_im.width):
        keypoint.append(cv.KeyPoint(c,r))
        """

        return gray
        
                
                
        
    
