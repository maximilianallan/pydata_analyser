#!/usr/bin/python

import cv,os,sys,string
from converter import converter

class image_getter:

    def __init__(self,root_dir = "."):
        
        self.root_dir = root_dir
        os.chdir(self.root_dir)
        self.im_stack = []
        self.mask_stack = []

    def run(self):
        
        self.get_fnames()
        
        if len(self.im_stack) == 0:

            print "Error, no images found"
            sys.exit(-1)

        convert = converter(self.im_stack,self.mask_stack)
        convert.parse_images()
        



    def get_fnames(self):

        for dset in os.listdir(os.getcwd()):
            
            if dset.find("data") == -1:
                continue

            self.parse_dir(dset)


    def parse_dir(self,dataset):
        
        for dirent in os.listdir(dataset):
            
            if dirent.find("training") >= 0:
                train_name = dirent
            if dirent.find("mask") >= 0:
                mask_name = dirent
                
        try:
            train_name
        except NameError:
            print "Error, training data directory not found or with bad name, include directory \"training_data\" for script to find"
            sys.exit(-1)

        try:
            mask_name
        except NameError:
            print "Error, mask directory not found or with bad name, include directory \"masks\" for script to find"
            sys.exit(-1)
            
            
        self.push_ims(dataset,train_name,mask_name)



    def push_ims(self, root_dir, train_name, mask_name):

        for image in os.listdir(root_dir + "/" + train_name):

            try:
                self.im_stack.append(cv.LoadImage(root_dir+"/"+train_name+"/"+image))
            except IOError:
                print "Error, " + image + " not found"
                continue

            try:
                self.mask_stack.append(cv.LoadImage(root_dir+"/"+mask_name+"/"+image))
            except IOError:
                print "Error, mask " + image + " not found"
                self.im_stack.pop()

        assert( len(self.im_stack) ==  len(self.mask_stack) ) 
            
        
        
if __name__ == '__main__':


    if len(sys.argv) < 2:
        print "bad cmd line args"
        sys.exit(-1)
        
    print "running"
    getter = image_getter(sys.argv[1])
    getter.run()
    print "done!"
