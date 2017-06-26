#coding=utf-8
__author__ = 'moonkey'

import os
import numpy as np
from PIL import Image
from collections import Counter
import pickle as cPickle
import random, math
from data_util.bucketdata import BucketData
import codecs
import cv2
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class DataGen(object):
	GO = 1
	EOS = 2
	#获得字对应的索引
	words =[]
	labels = []
	annotation_path1 = "word_label.txt"
	if os.path.isfile(annotation_path1):
		with codecs.open(annotation_path1, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			for l in lines:
				word, lex = l.strip().split() 
				words.append(word)
				labels.append(lex)
				#print (word.encode("utf-8"), lex)
	else:
		print ("File does not exist:{}".format(annotation_path1))
		
	
	def __init__(self,
				data_root, annotation_fn,
				evaluate = False,
				valid_target_len = float('inf'),
				img_width_range = (12, 320),
				word_len = 30):
		
		"""
		:param data_root:
		:param annotation_fn:
		:param lexicon_fn:
		:param img_width_range: only needed for training set
		:return:
		"""

		img_height = 32
		self.data_root = data_root
		if os.path.exists(annotation_fn):
			self.annotation_path = annotation_fn
		else:
			self.annotation_path = os.path.join(data_root, annotation_fn)

		if evaluate:
			self.bucket_specs = [(int(math.floor(64 / 4)), int(word_len + 2)), (int(math.floor(108 / 4)), int(word_len + 2)),
								(int(math.floor(140 / 4)), int(word_len + 2)), (int(math.floor(256 / 4)), int(word_len + 2)),
								(int(math.floor(img_width_range[1] / 4)), int(word_len + 2))]
		else:
			self.bucket_specs = [(int(64 / 4), 9 + 2), (int(108 / 4), 15 + 2),
								(int(140 / 4), 17 + 2), (int(256 / 4), 20 + 2),
								(int(math.ceil(img_width_range[1] / 4)), word_len + 2)]

		self.bucket_min_width, self.bucket_max_width = img_width_range
		self.image_height = img_height
		self.valid_target_len = valid_target_len

		self.bucket_data = {i: BucketData()
							for i in range(self.bucket_max_width + 1)}
		
		

	def clear(self):
		self.bucket_data = {i: BucketData()
							for i in range(self.bucket_max_width + 1)}

	def get_size(self):
		with codecs.open(self.annotation_path, 'r', "utf-8") as ann_file:
			return len(ann_file.readlines())
			
	def is_valid_data(self, img_path, word):
		index1 = img_path.find("_",0)
		index2 = len(img_path)-len(word)-5
		word = img_path[index1+1:index2]          
		if word.isalnum(): 
			#if word.isupper(): #全是大写为true
			word = word.lower()  #字符串里面可以有数字、大小写、别的符号              
			return img_path, word
		else:
			return img_path, None
			
			
	def gen(self, batch_size):
		valid_target_len = self.valid_target_len
		if not os.path.exists(self.annotation_path):
			print (self.annotation_path + "  is not exist!")
		#print ("image_path txt:{}".format(self.annotation_path))
		with codecs.open(self.annotation_path, 'rb', "utf-8") as ann_file:
			lines = ann_file.readlines()
			random.shuffle(lines)
			#print ("\n")
			for l in lines:
				img_path, lex = l.strip().split()
				#print img_path
				'''img_path, lex = self.is_valid_data(img_path, lex)
				#print img_path
				#print lex
				if lex==None:
					continue
				#print ("111111")'''
				#print ("22222222")
				try:
					img_bw, word = self.read_data(img_path, lex)
					if len(word)==0:
						continue
					
					if valid_target_len < float('inf'):
						word = word[:valid_target_len + 1]
					width = img_bw.shape[-1]

					# TODO:resize if > 320
					b_idx = min(width, self.bucket_max_width)
					bs = self.bucket_data[b_idx].append(img_bw, word, os.path.join(self.data_root,img_path))
					if bs >= batch_size:
						b = self.bucket_data[b_idx].flush_out(
								self.bucket_specs,
								valid_target_length=valid_target_len,
								go_shift=1)
						if b is not None:
							yield b
						else:
							assert False, 'no valid bucket of width %d'%width
				except IOError:
					#print ("111111111111")
					pass # ignore error images
					#with open('error_img.txt', 'a') as ef:
					#    ef.write(img_path + '\n')
		self.clear()
	
	def word_label(self, c): #获得word对应的label
		if c in self.words:
			label = self.words.index(c) #list.index()必须是list中包含的值，不然会抛出异常。
			if label > -1:
				return self.labels[label]
			
	def label_word(self, c):#获得label对应的word
		c = str(c)
		if c in self.labels:
			#print ("words len:{}".format(len(self.words)))
			label = self.labels.index(c)
			#print ("label index:{}".format(label))
			if label > -1:
				return self.words[label]
			
	
	def read_data(self, img_path, lex):
		assert 0 < len(lex) < self.bucket_specs[-1][1]
		#print ("root:{}".format(self.data_root))
		# L = R * 299/1000 + G * 587/1000 + B * 114/1000
		#print ("image:{}".format( img_path))
		#with codecs.open(os.path.join(self.data_root, img_path), 'rb', "utf-8") as img_file:
		if 1:
			img = cv2.imread(img_path)#img = Image.open(img_path)
			#w, h = img.size
			'''aspect_ratio = float(w) / float(h)
			if aspect_ratio < float(self.bucket_min_width) / self.image_height:
				img = img.resize(
					(self.bucket_min_width, self.image_height),
					Image.ANTIALIAS)
			elif aspect_ratio > float(
				self.bucket_max_width) / self.image_height:
				img = img.resize(
					(self.bucket_max_width, self.image_height),
					Image.ANTIALIAS)
			elif h != self.image_height:
				#img = img.resize((int(aspect_ratio * self.image_height), self.image_height),Image.ANTIALIAS)
				img = img.resize((100, 32),Image.ANTIALIAS)	'''
			img = cv2.resize(img, (100, 32))#img = cv2.resize(img, (100, 32))#img.resize((100, 32),Image.ANTIALIAS)	#	Image.BILINEAR) 

			img_bw = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)#img_bw = img.convert('L') #灰度化
			img_bw = np.asarray(img_bw, dtype=np.uint8)
			img_bw = img_bw[np.newaxis, :]

		# 'a':97, '0':48
		word = [self.GO]
		#print "\n"
		for c in lex:
			l = c.encode("raw_unicode_escape")
			#print l
			#print lex.encode("utf-8")
			#print l.decode("raw_unicode_escape").encode("utf-8")
			
			if 1:#c in self.words: 
				cc = c.encode("raw_unicode_escape")
				#print ("c:{}".format(c.encode("utf-8")))  #.encode("raw_unicode_escape")
				if cc.find("\u", 0) > -1:
					#print ll.encode("raw_unicode_escape")
					label = self.words.index(c)	
					if label > -1:
						#print label
						#print self.labels[label]
						word.append(self.labels[label])
						#print c.encode("utf-8")
				elif 96 < ord(c) < 123 or 47 < ord(c) < 58 or 64 < ord(c) < 91:
					c = c.lower()
					#print ("ord(c):{}".format(ord(c)))
					label = self.words.index(c)
					if label > -1:
						#print self.labels[label]
						word.append(self.labels[label])
						#print c.encode("utf-8")
			else:
				#print ("c111111 :{}".format(c.encode("utf-8"))) 
				#print ("111111111111")
				word = []
				return img_bw, word 
			
			
			'''
			if l.find("\u", 0) > -1:
				l = int(l[2:],16)
				if l>=19968 and l<=40869:
					word.append( l-19968 + 3)
			else:
				word = []
				return img_bw, word'''
			#print word 
			'''
			assert 96 < ord(c) < 123 or 47 < ord(c) < 58 
			word.append(
				ord(c) - 97 + 13 if ord(c) > 96 else ord(c) - 48 + 3)'''
			'''for c in lex:
			assert 96 < ord(c) < 123 or 47 < ord(c) < 58 or 64 < ord(c) < 91
			if 123 > ord(c) > 96:
				tmp = ord(c) - 97 + 13
			elif 64 < ord(c) < 91:
				tmp = ord(c) - 65 + 39
			else:
				tmp = ord(c) - 48 + 3
			word.append(tmp)'''
		
		word.append(self.EOS)
		word = np.array(word, dtype=np.int32)
		# word = np.array( [self.GO] +
		# [ord(c) - 97 + 13 if ord(c) > 96 else ord(c) - 48 + 3
		# for c in lex] + [self.EOS], dtype=np.int32)

		return img_bw, word


def test_gen():
	print('testing gen_valid')
	# s_gen = EvalGen('../../data/evaluation_data/svt', 'test.txt')
	# s_gen = EvalGen('../../data/evaluation_data/iiit5k', 'test.txt')
	# s_gen = EvalGen('../../data/evaluation_data/icdar03', 'test.txt')
	s_gen = EvalGen('../../data/evaluation_data/icdar13', 'test.txt')
	count = 0
	for batch in s_gen.gen(1):
		count += 1
		print(str(batch['bucket_id']) + ' ' + str(batch['data'].shape[2:]))
		assert batch['data'].shape[2] == img_height
	print(count)


if __name__ == '__main__':
	test_gen()
