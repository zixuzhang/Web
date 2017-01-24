#-*- coding: utf-8 -*-
# from zipfile import *
import zipfile
import os
from pymongo import MongoClient
import gridfs

from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

client = MongoClient('localhost', 27017)
db = client.zxjd_database
fs = gridfs.GridFS(db)

os.chdir('/home/zxjd/zxjd_Project')
if zipfile.is_zipfile('1-成都市双流壁挂热交换器有限责任公司.zip'):
	zf = zipfile.ZipFile('1-成都市双流壁挂热交换器有限责任公司.zip','r')
	for name in zf.namelist():
		if os.path.splitext(name)[1] == '.pdf'
		