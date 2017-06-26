#coding=utf-8
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import re


# ValueError: could not convert string to float: s 1.686864
# 原因在于文本中的数字间不是一个空格，可能是一个“tab"或多个空格；
def get_loss(f):
    lst = []
    lines = f.readlines()
    for l in lines:      
        if l.find("global", 10) > -1: #返回索引位置(从0开始)，如果找不到返回-1
            #print l
            index1 = l.find("loss", 10)
            index2 = l.find("perplexity", 10)
            loss_value = l[index1+4:index2].strip() #strip() 方法用于移除字符串头尾指定的字符（默认为空格）。          
            #print len(loss_value)
            #print loss_value
            lst.append( float(loss_value) )   
    
    return lst
 
def get_X(value):
    x = []
    for i in range(len(value)):
       x.append(i*2000) 
    return x
    

f_128 = open("/opt/zhangjing/ocr/Attention_OCR/Attention-OCR-new-version/model/log_05_25.txt", 'r')
f_256 = open("/opt/zhangjing/ocr/Attention_OCR/Attention-OCR-new-version/model/log_05_17+数字+大小写不分+83%（word）.txt", 'r')
f_512 = open("/opt/zhangjing/ocr/Attention_OCR/Attention-OCR-new-version/model/log_05_22+数字+大小写不分+512+83%（word）.txt", 'r')

loss_128 = []
loss_256 = []
loss_512 = []

# 
loss_128 = get_loss(f_128)
loss_256 = get_loss(f_256)
loss_512 = get_loss(f_512)
#print loss_512

plt.xlim(0, 50000)# set axis limits
plt.ylim(0.0, 2.)

x_128 = get_X(loss_128)
x_256 = get_X(loss_256)
x_512 = get_X(loss_512)

plt.plot(x_128, loss_128, 'r', label='128') #'ro' 红色 散点
plt.plot(x_256, loss_256, 'g', label='256')
plt.plot(x_512, loss_512, 'b', label='512')

plt.legend(loc='upper right', shadow=True, fontsize='x-large')# make legend

plt.title('loss & Number of hidden units') 
plt.xlabel('global step(+2000)')
plt.ylabel('loss')

plt.show()# show the plot on the screen
plt.savefig("loss_hidden.png")