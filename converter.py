#!/usr/bin/python

import cv,visualiser

class converter:


    def __init__(self, im_stack, mask_stack):

        self.im_stack = im_stack
        self.mask_stack = mask_stack
        self.converters.append(converter.rgb2rgb)
        self.converters.append(converter.rgb2hsv)
        self.converters.append(converter.rgb2cie)
        self.converters.append(converter.rgb2sift)

    def parse_images(self):

        for image in range(len(self.im_stack)):
            
            parse_pair(im_stack[image],mask_stack[image])

        
    def parse_pair(self,image,mask,convert):
        
        xyz = 2


    @staticmethod
    def rgb2rgb(in_im):
        return in_im;

    @staticmethod
    def rgb2hsv(in_im,out_im):
        out_im = cv.CreateMat(cv.GetSize(in_im),in_im.type_)
        cv2.cvtColor(in_im,out_im,cv.CV_RGB2HSV)
        return out_im


    @staticmethod
    def rgb2cie(in_im,out_im):
        out_im = cv.CreateMat(cv.GetSize(in_im),in_im.type_)
        cv2.cvtColor(in_im,out_im,cv.CV_RGB2XYZ)
        return out_im
    
    @staticmethod
    def rgb2sift(in_im,out_im):
        for r in range(in_im.rows):
            for c in range(in_im.cols):
                
        
    
