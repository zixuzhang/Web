from pymongo import MongoClient
import gridfs
import os
client = MongoClient('localhost', 27017)
db = client.zxjd_database
fs = gridfs.GridFS(db)
# files = fs.find()
# print files.count()
# os.chdir('/home/zxjd/file')
# for file in files:
# 	if file.filename.find('.doc') > 0:
# 		with open(file.filename, 'wb') as f1:
# 			f1.write(file.read())
file = fs.find_one('_id' = '5834f7d8968e4e19c8fc73c2')
os.chdir('/home/zxjd/file')
with open(file.filename, 'wb') as f1:
	f1.write(file.read())