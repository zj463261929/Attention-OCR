#coding=utf-8
import os

def is_valid_data(img_path, word):
        index1 = img_path.find("_",0)
        index2 = img_path.find("_",index1+1) #len(img_path)-len(word)-5
        word = img_path[index1+1:index2]          
        if word.isalnum(): 
            #if word.isupper() or word.istitle(): #全是大写为true
            word = word.lower() #                                
            return img_path, word
        else:
            return img_path, None
          

annotation_path = "/opt/ligang/data/pic2000_15_data_2017_5_31/result_img_word/WordBBText.txt"#"/opt/datasets/data/str/SynthTextforRecognition/train.txt" #"/opt/datasets/data/str/mnt/ramdisk/max/90kDICT32px/annotation_train_new.txt"
annotation_path1 = "/opt/datasets/data/str/mnt/ramdisk/max/90kDICT32px/annotation_new.txt"
#f = open(annotation_path1, 'w')

print os.path.isfile(annotation_path)

with open(annotation_path, 'r') as ann_file:
    lines = ann_file.readlines()
    #random.shuffle(lines)
    n = 0
    for l in lines:
        img_path, lex = l.strip().split() 
        #print ("\n")
        #print img_path
        #img_path, lex = is_valid_data(img_path, lex)
        #print img_path
       
        #print lex
        if lex==None:
            continue
        else:
            #查看txt数据集里面是否包含数字
            if lex.isdigit():
                n = n + 1
                print n
                print ("label:{}".format(lex))
            ''' lst = [img_path, lex]
            l = ' '.join(lst) #用空格重新组合
            #print l
            f.write(l)
            f.write("\n")
    
    f.close()'''