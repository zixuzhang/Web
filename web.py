# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix
from pymongo import MongoClient
# from flask_mongoengine import MongoEngine
from mongoengine import *
import gridfs
import os

connect('zxjd_project')

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# app.config.from_pyfile('the-config.cfg')
# db = MongoEngine(app)
client = MongoClient('localhost',27017)
db = client.zxjd_database
fs = gridfs.GridFS(db)



@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.route('/')
def index():
	files = fs.find()
	count = files.count()
	return render_template('project.html', count=count, files=files)

@app.route('/project')
def project():
	return render_template('project.html')

@app.route('/project/government') #zhengfu 
def government():
	return render_template('government.html')

@app.route('/project/innovation') #chuangxin
def innovation():
	return render_template('innovation.html')

@app.route('/project/investment') #touzi 
def investment():
	return render_template('investment.html')

class Project(Document):
	filename = StringField()
	file = FileField()


# @app.route('/<file_id>')
# def download(file_id):
# 	file = fs.find_one({"_id" : file_id })
# 	os.chdir('/home/zxjd/file')
# 	with open(file.filename, 'wb') as f1:
# 		f1.write(file.read())
# 	# return '<h1>%s!</h1>' % name

if __name__ == '__main__':
	manager.wsgi_app = ProxyFix(app.wsgi_app)
	manager.run()
	client = Mongoclient('localhost',27017)
	db = client.zxjd_database
	fs = gridfs.GridFS(db)