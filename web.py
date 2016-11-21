# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.route('/')
def index():
	return render_template('project.html')

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
#
# @app.route('/project/<name>')
# def project(name):
# 	return '<h1>%s!</h1>' % name

if __name__ == '__main__':
	manager.wsgi_app = ProxyFix(app.wsgi_app)
	manager.run()