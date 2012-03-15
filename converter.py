#!/usr/bin/python

import cv,cv2
from visualiser import visualiser

class converter:


    def __init__(self, im_stack, mask_stack):

        """
        set up the image and mask stack as well as add the convertion function
        pointers
        @param the stack of iplimages of frames 
        @param the stack of iplimages of masks
        """

        self.im_stack = im_stack
        self.mask_stack = mask_stack
        self.converters = []
        self.converters.append(converter.rgb2rgb)
        self.converters.append(converter.rgb2hsv)
        self.converters.append(converter.rgb2cie)
        #self.converters.append(converter.rgb2sift)
        self.converters.append(converter.opponent1)
        self.converters.append(converter.opponent2)
        self.converters.append(converter.norm_red)
        self.converters.append(converter.norm_green)

    def parse_images(self):

        """
        for each image and corresponding mask, convert the image according to
        function pointer funct and push the pixels into converter::class_pix 
        lists
        """

        vis = visualiser()

        for funct in self.converters:
            print "starting image..."
            #set up the pixel lists
           
            for image in range(int(float(len(self.im_stack))/3)):
                 self.parse_pair(self.im_stack[image],
                                 self.mask_stack[image],
                                 funct,image)
            
            print "got images..."

            for n in range(len(self.class_pix)):
                
                for chan in range(len(self.class_pix[n])):
                    vis.set_data(self.class_pix[n][chan])
                    vis.set_title("class {0} - channel {1}".format(n,chan))
                    print "drawing"
                    vis.draw()

                print "done one class..."
            #clear up list - is this necessary?        
            for n in range(len(self.class_pix)):
                for m in range(len(self.class_pix[n])):
                    del self.class_pix[n][m][:]
            
                

    def parse_pair(self,image,mask,convert,count):

        """
        convert an image according to function pointer convert and then push 
        the pixels into converter::class_pix
        @param image is the image to convert and take pixels from
        @param mask specifies which pixels to push into which list
        @param convert is a function pointer which converts features in image into
        a different represnetation based on color/gradients etc
        """
        print "converting image...",
        new_im = convert(image)
        print "done"
        #class_pix[n] has size(channels) lists of the pixel vals in the class n
        if count == 0:
            self.class_pix = [ [[] for i in range(new_im.nChannels)],
                               [[] for i in range(new_im.nChannels)] ]
            


        print "getting pixels...",
        self.get_pixels(new_im,mask)
        print "done"
        

    def get_pixels(self,image,mask):
        
        """
        get_pixels ---> push the pixels into list according to bitmask
        @param image is the image to take the pixels from
        @param mask is the bitmasks which specifies which list to push the pixels to
        @param class pix is a list of nested lists, each index of the list corresponds to a class and and the value associated with than index corresponds a list of channels each containing a list of pixels that have been allocated to that class by the bitmask
        """       
            
        if cmp(image.width,mask.width):
            return
        if cmp(image.height,mask.height):
            return

        for r in range(image.height):
            for c in range(image.width):
                pix = image[r,c]
                for n in range(image.nChannels):
                    #push pixels according to mask
                    if isinstance(pix,tuple):
                        pix_v = pix[n]
                    else:
                        pix_v = pix

                    if mask[r,c][n] == 255.0:
                        self.class_pix[0][n].append(pix_v)
                    else:
                        self.class_pix[1][n].append(pix_v)


                            
                     

    @staticmethod
    def rgb2rgb(in_im):
        return in_im;

    @staticmethod
    def rgb2hsv(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                in_im.depth,
                                in_im.nChannels)
        cv.CvtColor(in_im,out_im,cv.CV_RGB2HSV)
        return out_im


    @staticmethod
    def rgb2cie(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                in_im.depth,
                                in_im.nChannels)
        cv.CvtColor(in_im,out_im,cv.CV_RGB2XYZ)
        return out_im
    
    @staticmethod
    def rgb2sift(in_im):
        keypoint = []
        gray = cv.CreateImage(cv.GetSize(in_im),
                              in_im.depth,
                              1)
        cv.CvtColor(in_im,gray,cv.CV_RGB2GRAY)
        return gray


    @staticmethod
    def opponent1(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                cv.IPL_DEPTH_32F,
                                1)
        for r in range(in_im.height):
            for c in range(in_im.width):
                (r,g,b) = in_im[r,c]
                out_im[r,c] = 0.5*(r-g)
        return out_im

    @staticmethod
    def opponent2(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                cv.IPL_DEPTH_32F,
                                1)
        for r in range(in_im.height):
            for c in range(in_im.width):
                (r,g,b) = in_im[r,c]
                out_im[r,c] = 0.5*b - 0.25*(r+g)
        return out_im
                
    @staticmethod
    def norm_red(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                cv.IPL_DEPTH_32F,
                                1)
        for r in range(in_im.height):
            for c in range(in_im.width):
                (r,g,b) = in_im[r,c]
                if r+g+b == 0:
                    out_im[r,c] = 0.0000000001
                else:
                    out_im[r,c] = float(r)/(r+g+b)
        return out_im
                    
    @staticmethod
    def norm_green(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                cv.IPL_DEPTH_32F,
                                1)
        for r in range(in_im.height):
            for c in range(in_im.width):
                (r,g,b) = in_im[r,c]
                if r+g+b == 0:
                    out_im[r,c] = 0.0000000000001
                else:
                    out_im[r,c] = float(g)/(r+g+b)
        return out_im
    
                
                
        
    
        
