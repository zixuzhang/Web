# -*- coding: UTF-8 -*-

import os 

def getDirList(p):
	p = str(p)
	print p
	print p == ""
	if p == "":
		return []

	# if p[-1] !='/':
	# 	p = p +'/'
	a = os.listdir(p)
	b = [x for x in a if os.path.isdir(p + x)]
	return b 
print getDirList('/home/zxjd/zxjd_Project/')