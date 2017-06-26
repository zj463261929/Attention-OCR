#coding=utf-8
from math import ceil
import scipy.misc
from scipy.misc import imresize
import cv2
import sys
import os
import os.path
import string
import h5py
import numpy as np
from collections import namedtuple
import random
import time
import math
import traceback
import scipy.io as sio



def generate_dataset():
    
    total = 0
    images = 0 
    path_new = "/opt/datasets/data/str/SynthTextforRecognition"
    f = open(path_new+"/train.txt", 'w')
    '''i=1
    while i<201:
        os.mkdir(path_new + "/" + str(i))
        i = i+1'''
    
    try:
        db_location ="/opt/datasets/data/str/SynthText"
        in_db = sio.loadmat("/opt/datasets/data/str/SynthText/gt.mat")            
        '''print in_db.keys() 
        print in_db['wordBB'][0]
        print in_db['wordBB'][0][:]
        print len(in_db['wordBB'][0])
        print in_db['wordBB'][0][1]
        print len(in_db['wordBB'][0][1])
        print in_db['txt'][0][1]
        print in_db['wordBB'][0][2]
        print in_db['wordBB'][0][2].shape
        print in_db['txt'][0][2]'''
        
        imageNum = len(in_db['imnames'][0])
        print ("image num:{}".format(imageNum))      
        #imageNum = 1
        for index in np.arange(imageNum):#range(1) :
            ss = str(in_db['imnames'][0][index])
            image_path = ss[3:len(ss)-2]
            #print ("image path:{}".format(ss[3:len(ss)-2]))
            #print ("image path:{}".format(ss))  #[u'8/ballet_106_0.jpg']

            '''s2 = ss[3:len(ss)-2]
            if s2 != '182/turtles_44_14.jpg': #'8/ballet_131_35.jpg':
                continue'''
            
            strqq = db_location + "/" + image_path #ss[3:len(ss)-2]
            #print ("abs path:{}".format(strqq))
            
            #img = item[:].astype('float32')
            #print ("image path:{}\n".format(strqq))
                               
            img = cv2.imread(strqq)
            #image_src = img.copy()
                
            if img is not None:
                images +=1 
                print ("current image index:{}\n".format(images))

                # BBs and word labels are both lists where corresponding indices match
                wordBB = in_db['wordBB'][0][index] 
                words = in_db['txt'][0][index] 
                #print wordBB
                #print words #[u'Lines:\nI lost\nKevin' u'will' u'line\nand' u'and\nthe' u'(and' u'the\nout' u'you' u"don't\n pkg"]
                
                word_lst = []
                for l in words:
                    lst = []
                    lst = l.strip().split('\n')
                    for ll in lst:
                        lst2 = []
                        lst2 = ll.strip().split()  
                        for lll in lst2:
                            word_lst.append(lll)
                    
                #print len(word_lst)
                #print word_lst
                if len(wordBB.shape)==3:# and len(word_lst)==wordBB.shape[-1]:  
                    wordBBNum = wordBB.shape[-1]  
                    #print ("wordBBNum:{}".format(wordBBNum))                   
                    for i2 in xrange(min(wordBBNum,len(word_lst))):                                 
                        bb = wordBB[:,:,i2]                            
                        bb = np.c_[bb, bb[:,0]]                            
                                    
                        (tl, tr, br, bl) = bb[0:, 0:4].T
                        word = word_lst[i2]
                        #print word
                        
                        x_min = min(tl[0],tr[0],bl[0],br[0])
                        x_max = max(tl[0],tr[0],bl[0],br[0])
                        y_min = min(tl[1],tr[1],bl[1],br[1])
                        y_max = max(tl[1],tr[1],bl[1],br[1])
       
                        w = math.fabs(x_max - x_min)
                        h = math.fabs(y_max - y_min)
                        '''
                        cv2.rectangle(img,(int(x_min),int(y_min)),(int(x_max),int(y_max)),(0,0,255),1)
                        cv2.putText(img,word,(int(tl[0]),int(tl[1])),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,0),thickness=1,lineType=8)'''  
                        
                        if word.isalnum():
                            word = word.lower()
                            img_path = image_path[:len(image_path)-4] + "_" + word + "_" + str(i2) + ".jpg"
                            ss = path_new + "/" + img_path
                            
                            #print ss
                            cv2.imwrite(ss, img[int(y_min):int(y_max), int(x_min):int(x_max)])
                            lst = [img_path, word]
                            l = ' '.join(lst) #用空格重新组合
                            #print l
                            f.write(l)
                            f.write("\n")
                                      
                        #print ("src:tl,tr,bl,br:{}\n".format((tl[:],tr[:],bl[:],br[:])))
                                                 
                    total +=1           
    except:
      
        print("Error loading ")       
        
    f.close() 
    #print("Total number of ground truth images: " + str(images))

if __name__ == "__main__":
    generate_dataset()
