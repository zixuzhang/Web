#-*- coding: utf-8 -*-
import zipfile
import os, json
from pymongo import MongoClient
import gridfs 


d1={}
os.chdir('/home/zxjd/zxjd_Project')
if zipfile.is_zipfile('1-成都市双流壁挂热交换器有限责任公司.zip'):
	zf = zipfile.ZipFile('1-成都市双流壁挂热交换器有限责任公司.zip','r')
	zf.printdir()
	print zf