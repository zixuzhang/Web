#-*- coding: utf-8 -*-
import os

def doc2str(data):
    os.chdir('/home/zxjd/Web/cace')
    # name = name.encode('utf-8')
    name = 'a.doc'
    doc_file = open(name,'wb')
    doc_file.write(data)
    doc_file.close()
    # doc_file = '1-可行性报告.doc'
    text_file = '%s.text' % name
    os.system("catdoc %s > %s" % (name, text_file))
    f = open(text_file, 'r')
    content = f.read()
    # os.system('rm %s' % text_file)
    # os.system('rm %s' % name)
    # print content
    return content