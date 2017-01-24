#!/usr/bin/env pyton
#coding=utf-8
import sys, os
reload(sys)
sys.setdefaultencoding( "utf-8" )
import xlrd
os.chdir('/home/zxjd/Web/cace')

def xls2str(data):
    fname = 'a.xls'
    xls_file = open(fname, 'wb')
    xls_file.write(data)
    s=''
    #fname = "/u1/scripts/pc_report/pc.xlsx"
    # fname = sys.argv[1]    #命令行参数 ,取第一个参数

    # print  fname
    bk = xlrd.open_workbook(fname)
    #工作簿中所有sheet的名称
    #print bk.sheet_names()
    #shxrange = range(bk.nsheets)

    #循环获取每个sheet中的数据
    sheetnames = bk.sheet_names()
    for m in sheetnames:
        sh = bk.sheet_by_name(m)
        #获取行数
        nrows = sh.nrows
        #获取列数
        ncols = sh.ncols     #此行可注释掉
        #print "nrows %d, ncols %d" % (nrows,ncols)
        row_list = []
        #获取各行数据
        for i in range(nrows):
            row_data = sh.row_values(i)
            for j in range(len(row_data)):
                # print "\""+str(row_data[j])+"\"",
                s = s + "\""+str(row_data[j])+"\""
            # print ""  #输出每行后 换行
    return s
