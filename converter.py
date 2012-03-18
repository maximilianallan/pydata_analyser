#!/usr/bin/python

import cv,cv2
from visualiser import visualiser

class channel:
    def __init__(self, lo,hi,no_bins,name):
        self.range = (lo,hi)
        self.no_bins = no_bins
        self.name = name


class converter:

    def __init__(self, lo, hi, no_bins, channel_names,function):
        self.channels = []
        for i in range(len(lo)):
            self.channels.append( channel(lo[i],hi[i],no_bins[i],channel_names[i]) )
        self.convert = function

class converter_factory:


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
        self.converters.append(converter([0 for i in range(3)],
                                         [255 for i in range(3)],
                                         [256 for i in range(3)],
                                         ["blue","green","red"],
                                         converter_factory.bgr2bgr))
        self.converters.append(converter([0 for i in range(3)],
                                         [360,255,255],
                                         [360,256,256],
                                         ["hue","saturation","value"],
                                         converter_factory.bgr2hsv))
        self.converters.append(converter([0 for i in range(3)],
                                         [255 for i in range(3)],
                                         [256 for i in range(3)],
                                         ["X","Y","Z"],
                                         converter_factory.bgr2cie))
        #self.converters.append(converter.rgb2sift)
        self.converters.append(converter([-128],
                                         [128],
                                         [256],
                                         ["opponent 1"],
                                         converter_factory.opponent1))
        self.converters.append(converter([-125],
                                         [128],
                                         [254],
                                         ["opponent 2"],
                                         converter_factory.opponent2))
        self.converters.append(converter([0],
                                         [1],
                                         [255],
                                         ["normalized red"],
                                         converter_factory.norm_red))
        self.converters.append(converter([0],
                                         [1],
                                         [255],
                                         ["normalized green"],
                                         converter_factory.norm_green))

    def parse_images(self):

        """
        for each image and corresponding mask, convert the image according to
        function pointer funct and push the pixels into converter::class_pix 
        lists
        """

        vis = visualiser()
        class_names = ["tool","tissue"]

        for conv in self.converters:
            print "starting image..."
            #set up the pixel lists
            for s_image in range(int(float(len(self.im_stack))/3)):
                
                self.parse_pair(self.im_stack[s_image],
                                self.mask_stack[s_image],
                                conv.convert,s_image)

                            
            print "got images..."

            for n in range(len(self.class_pix)):
                
                for chan in range(len(conv.channels)):
                    vis.set_data(self.class_pix[n][chan])
                    assert(len(self.class_pix[n][chan]) > 0)
                    vis.set_title("class {0} - channel {1}".format(class_names[n],
                                                                   conv.channels[chan].name))
                    vis.set_bins(conv.channels[chan].no_bins)
                    vis.set_range(conv.channels[chan].range)
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

        for r in range(50,image.height-50):
            for c in range(50,image.width-50):
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
    def bgr2bgr(in_im):
        return in_im;

    @staticmethod
    def bgr2hsv(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                in_im.depth,
                                in_im.nChannels)
        cv.CvtColor(in_im,out_im,cv.CV_BGR2HSV)
        return out_im


    @staticmethod
    def bgr2cie(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                in_im.depth,
                                in_im.nChannels)
        cv.CvtColor(in_im,out_im,cv.CV_BGR2XYZ)
        return out_im
    
    @staticmethod
    def bgr2sift(in_im):
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
                (blue,green,red) = in_im[r,c]
                out_im[r,c] = 0.5*(red-green)
        return out_im

    @staticmethod
    def opponent2(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                cv.IPL_DEPTH_32F,
                                1)
        for r in range(in_im.height):
            for c in range(in_im.width):
                (blue,green,red) = in_im[r,c]
                out_im[r,c] = 0.5*blue - 0.25*(red+green)
        return out_im
                
    @staticmethod
    def norm_red(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                cv.IPL_DEPTH_32F,
                                1)
        for r in range(in_im.height):
            for c in range(in_im.width):
                (blue,green,red) = in_im[r,c]
                if red+green+blue == 0:
                    out_im[r,c] = 0.0000000001
                else:
                    out_im[r,c] = float(red)/(red+green+blue)
        return out_im
                    
    @staticmethod
    def norm_green(in_im):
        out_im = cv.CreateImage(cv.GetSize(in_im),
                                cv.IPL_DEPTH_32F,
                                1)
        for r in range(in_im.height):
            for c in range(in_im.width):
                (blue,green,red) = in_im[r,c]
                if red+green+blue == 0:
                    out_im[r,c] = 0.0000000000001
                else:
                    out_im[r,c] = float(green)/(red+green+blue)
        return out_im
    
                
                
        
    
        
