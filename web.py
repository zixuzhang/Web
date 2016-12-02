# -*- coding: utf-8 -*-
from flask import Flask, render_template, make_response, request, url_for, redirect
from flask_script import Manager
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import os, StringIO, zipfile, sys ,chardet

# connect('zxjd_project')

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
client = MongoClient('localhost',27017)
db = client.zxjd_database
fs = gridfs.GridFS(db)


class Project(Document):
	filename = StringField()
	file = FileField()

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
	return render_template('index.html', count=count, files=files)

#公司列表
@app.route('/company')
def company():
	company = fs.find().distinct('company_name')
	return render_template('company.html',company=company)

@app.route('/project')
def project():
	return render_template('index.html')

# @app.route('/project/government') #政府项目
# def government():
# 	return render_template('government.html')
#
# @app.route('/project/innovation') #创新主提
# def innovation():
# 	return render_template('innovation.html')
#
# @app.route('/project/investment') #投融资机构
# def investment():
# 	return render_template('investment.html')

#下载单个文件
@app.route('/<file_id>')
def download(file_id):
	file = fs.get(ObjectId(file_id))
	response = make_response(file.read())
	response.mimetype = 'application/octet-stream'
	filename = file.filename.encode('utf-8')
	response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
	return response

#上传压缩包
@app.route('/upload',methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		files = request.files.getlist("file")
		for file in files:
			if zipfile.is_zipfile(file):
				zf = zipfile.ZipFile(file, 'r')
				for name in zf.namelist():
					if isinstance(name, str):
						charset = chardet.detect(name)['encoding']
						if chardet.detect(name)['encoding'] == 'GB2312':
							name1 = unicode(name, 'GBK').encode('utf-8')
						else:
							name1 = name
					else:
						name1 = name
					if not name1[-1] == '/':
						c = name1.split('/')
						company_name = c[0]
						filename = c[-1]
						tag1 = c[1]
						data = zf.read(name)
						fs.put(data,filename=filename,company_name=company_name, tag1=tag1)
				return redirect(url_for('index'))
	return render_template('upload.html')

#客户（公司）主页
@app.route('/company/<company_name>')
def company_name(company_name):

	return render_template('company_name.html', company_name=company_name)

#查询数据网页
@app.route('/company/<company_name>/query_web')
def query_web(company_name):
	files = fs.find({'company_name':company_name, 'tag1':'查询数据-网页'})
	count = files.count()
	return render_template('query_web.html', company_name=company_name, files=files, count=count)

#查询数据专利
@app.route('/company/<company_name>/query_patent')
def query_patent(company_name):
	files = fs.find({'company_name':company_name, 'tag1':'查询数据-专利'})
	count = files.count()
	return render_template('query_patent.html', company_name=company_name, files=files, count=count)

#待处理文件
@app.route('/company/<company_name>/todo')
def todo(company_name):
	files = fs.find({'company_name':company_name, 'tag1':'待处理'})
	count = files.count()
	return render_template('todo.html', company_name=company_name, files=files, count=count)

#公司项目
@app.route('/company/<company_name>/company_project')
def company_project(company_name):
	files = fs.find({'company_name':company_name, 'tag1':'企业项目资料'})
	count = files.count()
	return render_template('company_project.html', company_name=company_name, files=files, count=count)

#公司信息
@app.route('/company/<company_name>/company_infor')
def company_infor(company_name):
	files = fs.find({'company_name':company_name, 'tag1':'企业基本信息'})
	count = files.count()
	return render_template('company_infor.html', company_name=company_name, files=files, count=count)


if __name__ == '__main__':
	# manager.wsgi_app = ProxyFix(app.wsgi_app)
	manager.run()
	# client = Mongoclient('localhost',27017)
	# db = client.zxjd_database
	# fs = gridfs.GridFS(db)