#coding=utf-8
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import re

path = "annotation_train_new.txt"
letter_path = "annotation_train_new_letter.txt"
word_path = "annotation_train_new_word.txt"

fw_letter = open(letter_path, 'w')
fw_word = open(word_path, 'w')


with open(path,'r') as f:
	lines = f.readlines()
	
	#统计word的频率
	lst1 = []
	for l in lines:
		img_path, lex = l.strip().split() 
		lex = lex.lower()
		lst1.append(lex)
	lst = list(set(lst1))#list(set(lst)) 去除列表中重复的元素
	
	pw = [0]*len(lst)
	i = 0
	s = " ".join(lst1)
	
	for word in lst:
		pw[i] = s.count(word)
		fw_word.write(word + " " + str(pw[i]) + '\n')
		i = i + 1
		
		
	#求方差
	N = len(lst)
	y1 = []
	for i in range(N):
		y1.append(pw[i])
		
	narray=np.array(y1)
	sum1=narray.sum()
	narray2=narray*narray
	sum2=narray2.sum()
	mean=sum1/N
	var=np.sqrt(sum2/N-mean**2)
	fw_word.write("mean" + " " + str(mean) + '\n')
	fw_word.write("var" + " " + str(var) + '\n')
	fw_word.close()
	
	#画字母频率的图
	pMin = min(pw)
	pMax = max(pw)
	
	plt.xlim(0, N)# set axis limits
	plt.ylim(pMin, pMax)

	y = []
	x = []
	for i in range(N):
		y.append(pw[i])
		x.append(i)
	
	
	plt.bar(x, y, facecolor='red', width=1)#plot(x,y,'r') #
	for i in range(N):
		plt.text(x[i]+0.6, y[i]+0.05, '%s' % lst[i], ha='center', va= 'bottom')
	
	plt.title('word & frequency') 
	plt.xlabel('word')
	plt.ylabel('frequency')

	#plt.show()# show the plot on the screen
	plt.savefig("word_frequency.png")
	print ("Statistics word frequency ok!")
	
	
	
	
	#统计字母的频率及画图
	p = [0]*(26+10)
	for l in lines:
		img_path, lex = l.strip().split() 
		lex = lex.lower()
		for c in lex:
			if 47 < ord(c) < 58:
				n = ord(c)-48
				p[n] = p[n] + 1
			elif 96 < ord(c) < 123: 
				n = ord(c) - 97 + 10
				p[n] = p[n] + 1
				
	#写字母频率到文件中、并求方程
	ave = 0
	xc = []
	for i in range(26+10):
		c = 0
		if -1 < i < 10:
			c = chr(i+48)
			xc.append(c)
		elif 9 < i < 26+10:
			c = chr(i-10 + 97)
			xc.append(c)
		fw_letter.write(str(c) + " " + str(p[i]) + '\n')
		
	print (len(xc))
	
	#求方差
	y1 = []
	for i in range(26+10):
		y1.append(p[i])
	
	N = 26+10
	narray=np.array(y1)
	sum1=narray.sum()
	narray2=narray*narray
	sum2=narray2.sum()
	mean=sum1/N
	var=np.sqrt(sum2/N-mean**2)
	fw_letter.write("mean" + " " + str(mean) + '\n')
	fw_letter.write("var" + " " + str(var) + '\n')
	fw_letter.close()
		
	#画字母频率的图
	pMin = min(p)
	pMax = max(p)
	
	plt.xlim(0, 26+10)# set axis limits
	plt.ylim(pMin, pMax)

	y = []
	x = []
	for i in range(26+10):
		y.append(p[i])
		x.append(i)
	
	
	plt.bar(x, y, facecolor='red', width=1)#plot(x,y,'r') #
	for i in range(26+10):
		plt.text(x[i]+0.6, y[i]+0.05, '%s' % xc[i], ha='center', va= 'bottom')
	
	plt.title('letter & frequency') 
	plt.xlabel('letter')
	plt.ylabel('frequency')

	#plt.show()# show the plot on the screen
	plt.savefig("letter_frequency.png")
	print ("Statistics letter frequency ok!")
	
	