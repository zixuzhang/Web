# -*- coding: utf-8 -*-
import json, re, sys, zipfile, chardet, gridfs, tika,logging
from flask import render_template, make_response, request, url_for, redirect, \
	flash, jsonify, abort, session
from flask_login import login_required,current_user
from flask_paginate import Pagination
tika.initVM()
from . import main
from .forms import UploadForm
from ..models import Files, Nodes,Manage
from app.file_parse.file_parse import File_Parse
from app.filedata_manage.filedata_manage import fulltext_search1, fulltext_search, fulltext_search_all

# from .. import fs, categories,share_collection
# from bson.objectid import ObjectId
# from pymongo import MongoClient

#解决flash字符编码问题
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

sys.setrecursionlimit(10000)

#根路由
@main.route('/')
def index():
	page = request.args.get('page', type=int, default=1)
	skip = (page - 1) * 25
	# files = fs.find({'filename':{"$ne":''}}).skip(skip).limit(25)
	files = Files.objects().skip(skip).limit(25)
	count = files.count()
	pagination = Pagination(page=page, total=count, css_framework='bootstrap3',per_page=25)
	return render_template('index.html', count=count, files=files,
						   pagination=pagination)


#下载单个文件
@main.route('/download/<file_id>')
@login_required
def download(file_id):
	file = Files.objects.get(id=file_id)
	response = make_response(file.filedata.read())
	response.mimetype = 'application/octet-stream'
	filename = file.filename.encode('utf-8')
	response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
	return response

@main.route('/img/<img_id>')
def img(img_id):
	file = Files.objects.get(id=img_id)
	pass

#单文件的删除
@main.route('/delete/<file_id>')
@login_required
def file_delete(file_id):
	file = Files.objects.get(id=file_id)
	filename = file.filename
	Files.delete(file)
	flash(filename + '已删除')
	return redirect(url_for('main.user'))

#更新文件
@main.route('/update_file',methods=['GET','POST'])
@login_required
def file_update():
	if request.method == 'POST':
		new_file = request.files['file']
		file_id = request.form.get('file_id')
		filename =new_file.filename
		data = new_file.read()
		file_parse = File_Parse(filename, data)
		text, html, status = file_parse.parse()
		file = Files.objects.get(id=file_id)
		file.update(filename=filename,status=status,text=text, html=html)
		file.filedata.replace(data)
		return '更新成功'

# 全文搜索
@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	user = current_user
	email = user.email
	library = Files.objects.distinct('library')
	if request.method == 'POST':
		search_name = request.form.get('search_name')
		library_search = request.form.get('library')
		option = request.form.get('option')
		dict1 = Files().search(library_search,option,search_name)
		dict1['library_search'] = u'你好'
		dict1['option'] = option
		dict1['search_name'] = search_name
	return jsonify(dict1)

# @main.route('/full_text/search1', methods=['GET', 'POST'])
# def full_search1():
# 	company = fs.find().distinct('company_name')
# 	if request.method == 'POST':
# 		search_name = request.form.get('search_name')
# 		option = request.form.get('option')
# 		session['search_name'] = search_name
# 		session['option'] = option
# 		if search_name:
# 			if option == u'搜索全部文件':
# 				files = fs.find({"$or":[{'html': re.compile(search_name)},{'filename': re.compile(search_name)}]})
# 			elif option == u'搜索文件名':
# 				files = fs.find({'filename': re.compile(search_name)}).limit(13)
# 				files_list, count, match_count = fulltext_search_all(files)
# 				return render_template('full_search1.html', company=company, files_list=files_list,
# 									   count=count, match_count=match_count, option=session['option'])
# 			else:
# 				files = fs.find({"$or":[{'html': re.compile(search_name)},{'filename': re.compile(search_name)}],'company_name':option})
# 			files_list, count, match_count = fulltext_search1(files, search_name)
# 			return render_template('full_search1.html', search_name=search_name, company=company, files_list = files_list,
# 								   count = count, match_count = match_count, option=session['option'])
# 		else:
# 			files = fs.find({'filename': {"$ne": ''}})
# 			files_list, count, match_count = fulltext_search_all(files)
# 			return render_template('full_search1.html', company=company, files_list=files_list,
# 								   count=count, match_count=match_count)
# 	return render_template('full_search1.html', company=company, option='搜索全部文件')



#在当前文件夹下上传文件
@main.route('/add_file', methods=['GET', 'POST'])
@login_required
def add_file():
	user= current_user
	if request.method == 'POST':
		# file = request.files['file']
		files = request.files.getlist("file")
		# filename = file.filename
		tag = request.form.get('tag').split('/')
		# file_md5 = request.form.get('file_md5')
		library = tag[0]
		if files:
			for file in files :
				if Files.objects(tag=tag, author=user.email, library=library,filename=file.filename).first():
					# flash(file.filename + '在当前目录下已存在！')
					# return redirect(url_for('main.user'))
					# return render_template('user.html')
					return file.filename + '在当前目录下已存在！'
				else:
					filename = file.filename
					data = file.read()
					file_parse = File_Parse(filename, data)
					text, html, status = file_parse.parse()
					Files(filedata=data, filename=filename, library=library, tag=tag,
						  status=status, author=current_user.email).save()
					# return render_template('user.html')
			return '添加成功！'


#上传压缩包 并把压缩文件的层级结构存储到categories表中，把文件和文件的路径标签存储到GridFS
@main.route('/upload',methods=['GET','POST'])
@login_required
def upload():
	if request.method == 'POST':
		user = current_user
		email = user.email
		# files = request.files.getlist("file")
		file = request.files['file']
		file_md5 = request.form.get('file_md5')
		msg = Manage().upload(file, email, library_md5=file_md5)
		return msg


#ajax返回html字段进行预览
@main.route('/query_html')
def query_html():
	file_id = request.args.get('file_id')
	# file = fs.get(ObjectId(file_id))
	file = Files.objects(id=file_id).first()
	json_pre = {'html1':file.html,'filename':file.filename}
	return jsonify(json_pre)

#ajax查询各个文件夹下的文件
@main.route('/get_files')
def query():
	# tag = "9-成都酉辰科技有限公司/企业项目资料/2-技术附件"
	tag = request.args.get('tag', '')
	tag_list = tag.split('/')
	# files = fs.find({'filename': {"$ne": ''}, 'tag': tag})
	files = Files.objects(tag=tag_list)
	count = files.count()
	json_file = {'count':count}
	a=[]
	for file in files:
		a.append({'filename':file.filename,'file_id':str(file.id),'status': file.status})
	json_file['lists'] = a
	return jsonify(json_file)




# 分享 链接中查询文件
@main.route('/get_files1')
def query1():
	share_md5 = request.args.get('share_md5','')
	# tag1 = share_collection.find_one({'share_md5':share_md5})["tag"]
	tag1 = Nodes.objects(share_md5=share_md5).first().node
	l = tag1[:-1]
	tag_prents = '/'.join(l)
	if tag_prents == '':
		tag_str = request.args.get('tag', '')
		tag = tag_str.split('/')
	else:
		tag_str = tag_prents + '/' + request.args.get('tag', '')
		tag = tag_str.split('/')
	# tag = "9-成都酉辰科技有限公司/企业项目资料/2-技术附件"
	# files = fs.find({'filename': {"$ne": ''}, 'tag': tag})
	files = Files.objects(tag=tag)
	count = files.count()
	json_file = {'count':count}
	a=[]
	for file in files:
		a.append({'filename':file.filename,'file_id':str(file.id)})
	json_file['lists'] = a
	return jsonify(json_file)

#ajax获取文件目录信息json
# @main.route('/get_json/<company_name>')
# def get_json(company_name):
# 	# 从categories表中生成关于文件结构的json数据，采用递归生成
# 	def json_tree(field):
# 		d = {'text': field[-1]}
# 		d['children'] = [json_tree(x["field"]) for x in categories.find({'path':field })]
# 		return d
# 	return json.dumps(json_tree([company_name]))

# ajax 分享 获取 树状信息
# @main.route('/get_folder_json/<field>')
# def get_folder_json(field):
# 	field_list = field.split(',')
# 	def json_tree(field):
# 		d = {'text': field[-1]}
# 		d['children'] = [json_tree(x["field"]) for x in categories.find({'path':field })]
# 		return d
# 	return json.dumps(json_tree(field_list))

#ajax 获取情报库的树状信息 或者根据具体的节点获取子节点的树状信息
@main.route('/get_folder_json/<node_arg>')
def get_folder_json(node_arg):
	node_list = node_arg.split(',')
	def json_tree(node):
		d = {'text': node[-1]}
		d['children'] = [json_tree(x.node) for x in Nodes.objects(parent_node=node)]
		return d
	return json.dumps(json_tree(node_list))

# ajax 获取分享链接
@main.route('/get_share_link')
@login_required
def get_share_link():
	user = current_user
	author = user.email
	tag = request.args.get('tag', '')
	node=tag.split('/')
	folder_node = Nodes.objects(author=author, node=node).first()
	if folder_node.share_status:
		share_md5 = folder_node.share_md5
		share_code = folder_node.share_code
	else:
		share_md5, share_code = folder_node.share()
	share_link = request.url_root + 'share/' + share_md5
	return jsonify({'share_link':share_link,'share_code':share_code})

@main.route('/delete_share', methods=['GET','POST'])
@login_required
def delete_share():
	email = current_user.email
	share_md5 = request.values.get('share_md5', '')
	Nodes.objects(author=email, share_md5=share_md5).first().delete_share()
	return ''

@main.route('/delete_node',methods=['GET','POST'])
@login_required
def delete_node():
	user = current_user
	author = user.email
	node = request.args.get('tag', '').split('/')
	Nodes.objects(author=author,node=node).first().delete_node(node)
	return ""

@main.route('/rename_node', methods=['GET','POST'])
@login_required
def rename_node():
	user = current_user
	if request.method == 'POST':
		rename = request.form.get('rename', '')
		tag = request.form.get('tag', '')
		node = tag.split('/')
		k = rename_where = len(node)-1
		Nodes.objects(author=user.email, node=node).first().rename_node(node, rename, k)
	return ''

@main.route('/new_node', methods=['GET','POST'])
@login_required
def new_node():
	user = current_user
	if request.method == 'POST':
		name = request.form.get('name','')
		tag = request.form.get('tag','')
		node = tag.split('/')
		Nodes.objects(author=user.email, node=node).first().new_node(node, name, user.email)
	return ''

@main.route('/home')
@login_required
def user():
	user = current_user
	form = UploadForm()
	email = user.email
	library = Nodes.objects(author=email,parent_node=[]).distinct('node')
	library1 = Nodes.objects(author=email, parent_node=[]).distinct('node')
	return render_template('user.html',form=form, library=library, library1=library1)

@main.route('/share')
@login_required
def share_list():
	user = current_user
	email = user.email
	share_list = Nodes.objects(author=email, share_status=True)
	count = share_list.count()
	share_link_root = request.url_root + 'share/'
	return render_template('share_list.html', share_list=share_list, share_link_root=share_link_root ,count=count)

@main.route('/share/<share_md5>', methods=['GET','POST'])
def share(share_md5):
	folder_node = Nodes.objects(share_md5=share_md5).first()
	if request.method == 'POST':
		share_code = request.form.get('share_code')
		if share_code == folder_node.share_code:
			field_str = folder_node.share_node.replace('/',',')
			return render_template('share_look.html' ,field_str = field_str, share_md5 = share_md5)
		flash('密码错误！')
	if folder_node.share_status:
		return render_template('share.html')
	else:
		abort(404)


