# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import gridfs
import os

# def get_db():

# 	client = MongoClient('localhost', 27017)
# 	db = client.zxjd_database
# 	#collection = db.test_collection
# 	return db
# def get_fs():

# 	fs = gridfs.GridFS(get_db())
# 	return fs

# rootdir = '/home/zxjd/zxjd_Project'

# def my_insert(rootdir):
# 	for root, dirs, files in os.walk(rootdir):
# 		for name in files:
# 			fs.put(name)
# 			#print os.path.join(root, name)

# if __name__ == "__main__":
# 	db = get_db()
# 	fs = get_fs
# 	my_insert(rootdir)
client = MongoClient('localhost',27017)
db = client.zxjd_database
fs = gridfs.GridFS(db)

rootdir = '/home/zxjd/zxjd_Project'

for root, dirs, files in os.walk(rootdir):
	for name in files:
		os.chdir(root)
		file = open(name,"rb")
		fs.put(file, filename = name)
		file.close()
		# print root
		print name

