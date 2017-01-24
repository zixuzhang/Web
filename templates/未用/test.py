# #下载查询数据-网页下的压缩包
# @app.route('/download_zip/<company_name>/query_web/<file>')
# def download_zip(company_name, file):
# 	files = fs.find({'filename': {"$ne": ''}, 'company_name': company_name, 'tag1':'查询网页-数据', 'tag2':file})
# 	f = zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED)
# 	for file1 in files:
# 		f.write(file1.read())
# 	f.close()
# 	data = zipfile.ZipFile(file, 'r')
# 	response = make_response(data)
# 	response.mimetype = 'application/octet-stream'
# 	filename = file.encode('utf-8')
# 	response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
# 	return response

#导航栏政府项目路由
# @app.route('/project/government')
# def government():
# 	return render_template('government.html')
#
#导航栏创新主题路由
# @app.route('/project/innovation') #创新主提
# def innovation():
# 	return render_template('innovation.html')
#
#导航栏投融资机构路由
# @app.route('/project/investment')
# def investment():
# 	return render_template('investment.html')


#版本1.02
# #客户（公司）主页
# @app.route('/company/<company_name>')
# def company_name(company_name):
# 	tags = fs.find({'company_name': company_name}).distinct('tag1')
# 	tt = tags[0]
# 	if tt=='查询数据-网页':
# 		tags2 = fs.find({'company_name': company_name, 'tag1': '查询数据-网页'}).distinct('tag2')
# 		count = len(tags2)
# 		return render_template('query_web_list.html', company_name=company_name, files=tags2, count=count, tags=tags,
# 							   t=tt)
# 	else:
# 		files = fs.find({'filename':{"$ne":''},'company_name': company_name, 'tag1':tt})
# 		count = files.count()
# 		return render_template('query.html', company_name=company_name, files=files, count=count, tags=tags, t=tt)

#公司分类一级标签下的文件信息
# @app.route('/company/<company_name>/<tag1>')
# def query_com(company_name,tag1):
# 	tags = fs.find({'company_name': company_name}).distinct('tag1')
# 	if tag1=='查询数据-网页':
# 		tags2 = fs.find({'company_name': company_name, 'tag1':'查询数据-网页'}).distinct('tag2')
# 		count = len(tags2)
# 		return render_template('query_web_list.html', company_name=company_name, files=tags2, count=count, tags=tags, t=tag1)
# 	else:
# 		files = fs.find({'filename':{"$ne":''},'company_name':company_name, 'tag1':tag1})
# 		count = files.count()
# 		return render_template('query.html', company_name=company_name, files=files, count=count, tags=tags, t=tag1)
#
# #企业项目资料分类
# @app.route('/company/<company_name>/project')
# def com_project(company_name):
# 	tdict = {}
# 	tags2 = fs.find({'company_name': company_name, 'tag1':'企业项目资料'}).distinct('tag2')
# 	for tag in tags2:
# 		tags3 = fs.find({'company_name': company_name, 'tag1':'企业项目资料', 'tag2':tag}).distinct('tag3')
# 		tdict[tag]=tags3
#
# 	files = fs.find({'filename':{"$ne":''},'company_name': company_name, 'tag1':'企业项目资料'})
# 	count = files.count()
# 	return render_template('com_project.html', company_name=company_name, files=files, count=count, tdict=tdict)
#
# #二级标签下的文件信息 查询项目资料的分类总内容
# @app.route('/company/<company_name>/project/<tag2>')
# def query_com_pro_all(company_name,tag2):
# 	tdict = {}
# 	tags2 = fs.find({'company_name': company_name, 'tag1': '企业项目资料'}).distinct('tag2')
# 	for tag in tags2:
# 		tags3 = fs.find({'company_name': company_name, 'tag1': '企业项目资料', 'tag2': tag}).distinct('tag3')
# 		tdict[tag] = tags3
# 	files = fs.find({'filename': {"$ne": ''}, 'company_name': company_name, 'tag1': '企业项目资料', 'tag2':tag2})
# 	count = files.count()
# 	return render_template('com_project.html', company_name=company_name, files=files, count=count, tdict=tdict)
#
# #三级标签下的文件信息 查询项目资料分类的分类内容
# @app.route('/company/<company_name>/project/<tag2>/<tag3>')
# def query_com_pro(company_name,tag2,tag3):
# 	tdict = {}
# 	tags2 = fs.find({'company_name': company_name, 'tag1': '企业项目资料'}).distinct('tag2')
# 	for tag in tags2:
# 		tags3 = fs.find({'company_name': company_name, 'tag1': '企业项目资料', 'tag2': tag}).distinct('tag3')
# 		tdict[tag] = tags3
# 	files = fs.find({'filename': {"$ne": ''}, 'company_name': company_name, 'tag1': '企业项目资料', 'tag2':tag2, 'tag3':tag3})
# 	count = files.count()
# 	return render_template('com_project.html', company_name=company_name, files=files, count=count, tdict=tdict)


#版本1.01
# #查询数据网页
# @app.route('/company/<company_name>/query_web')
# def query_web(company_name):
# 	files = fs.find({'company_name':company_name, 'tag1':'查询数据-网页'})
# 	count = files.count()
# 	return render_template('query_web.html', company_name=company_name, files=files, count=count)
#
# #查询数据专利
# @app.route('/company/<company_name>/query_patent')
# def query_patent(company_name):
# 	files = fs.find({'company_name':company_name, 'tag1':'查询数据-专利'})
# 	count = files.count()
# 	return render_template('query_patent.html', company_name=company_name, files=files, count=count)
#
# #待处理文件
# @app.route('/company/<company_name>/todo')
# def todo(company_name):
# 	files = fs.find({'company_name':company_name, 'tag1':'待处理'})
# 	count = files.count()
# 	return render_template('todo.html', company_name=company_name, files=files, count=count)
#
# #公司项目
# @app.route('/company/<company_name>/company_project')
# def company_project(company_name):
# 	files = fs.find({'company_name':company_name, 'tag1':'企业项目资料'})
# 	count = files.count()
# 	return render_template('company_project.html', company_name=company_name, files=files, count=count)
#
# #公司信息
# @app.route('/company/<company_name>/company_infor')
# def company_infor(company_name):
# 	files = fs.find({'company_name':company_name, 'tag1':'企业基本信息'})
# 	count = files.count()
# 	return render_template('company_infor.html', company_name=company_name, files=files, count=count)
