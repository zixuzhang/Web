#-*- coding: utf-8 -*-
# from zipfile import *
import zipfile
import os

os.chdir('/home/zxjd/zxjd_Project')
if zipfile.is_zipfile('1-成都市双流壁挂热交换器有限责任公司.zip'):
	zf = zipfile.ZipFile('1-成都市双流壁挂热交换器有限责任公司.zip','r')
	for name in zf.namelist():
		if not name[-1] == '/':
			print name[-1]多文件多文件的的的
			print name
	
