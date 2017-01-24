#-*- coding: utf-8 -*-
import zipfile
import os, json
from pymongo import MongoClient
import gridfs 


d1=[]
os.chdir('/home/zxjd/zxjd_Project')
if zipfile.is_zipfile('chengdushuangliubigua.zip'):
	zf = zipfile.ZipFile('chengdushuangliubigua.zip','r')
	for name in zf.namelist():
		if name[-1] == '/':
			print name
			name
			c = name.split('/')
			d1.append(c)
	d2 = str(d1).encode('utf-8')
	# print d2
	a = d1[0][0]
	c = [a]
	for x in d1:
		if x[0] != a :
			c.append(x[0])
	print c 

	
	# print json.dumps(d1, encoding="UTF-8", ensure_ascii=False)

			

