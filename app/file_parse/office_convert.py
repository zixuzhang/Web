# -*- coding: utf-8 -*-
#使用unoconv对office文件转换成html
import os, subprocess
basedir = os.path.abspath(os.path.dirname(__file__))
os.chdir(basedir + '/cace')

def convert(filetype):
    rename = 'a' + filetype
    cmd ="unoconv -f html %s" % rename
    subprocess.call(cmd, shell=True)
    html_name = 'a' + '.html'
    file_html = open(html_name, 'r')
    html_data = file_html.read()
    file_html.close()
    # os.remove(rename)
    # os.remove(html_name)
    return html_data
