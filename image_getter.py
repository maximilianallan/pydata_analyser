#!/usr/bin/python

import cv,os,sys,string,converter

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

        else:
            print "Done!"



    def get_fnames(self):

        for dset in os.listdir(os.getcwd()):
            
            if dset.find("data") == -1:
                continue

            self.parse_dir(dset)


    def parse_dir(self,dataset):
        
        for dirent in os.listdir(dataset):
            
            if dirent.find("training"):
                train_name = dirent
            if dirent.find("mask"):
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
                self.im_stack.append(cv.LoadImageM(root_dir+"/"+train_name+"/"+image))
                self.mask_stack.append(cv.LoadImageM(root_dir+"/"+mask_name+"/"+image))
            except IOError:
                print "Error, " + image + " not found"

        print "done"

            
        
        
if __name__ == '__main__':


    if len(sys.argv) < 2:
        print "bad cmd line args"
        sys.exit(-1)

    getter = image_getter(sys.argv[1])
    getter.run()
