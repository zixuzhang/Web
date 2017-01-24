# -*- coding: utf-8 -*-
import docx2txt, office_convert, pdftostr, xls2str, xlsx2str, doc2str
import tika, magic
tika.initVM()
from tika import parser
import os, StringIO, logging, chardet

class File_Parse():
    '''
    os.chdir('/home/zxjd/Web/cace')
    支持以下文档：
    ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', 'txt']
    具有解析文件和生成文件的功能，解析生成text和hmtl
    接收从zipfile模块中读取的文件数据（filedata）和读取的文件名字（filename）
    '''
    def __init__(self,filename,filedata):
        self.filename = filename
        self.filedata = filedata
        self.filetype = os.path.splitext(filename)[1]
        os.chdir('/home/zxjd/Web/cace')

    # 生成文件
    def create_file(self):
        name = 'a' + self.filetype
        xfile = open(name, 'wb')
        xfile.write(self.filedata)
        xfile.close()
        logging.info('生成原始文件')

    # 删除文件
    def delete_file(self):
        logging.info('删除文件')
        filetype = self.filetype.lower()
        name = 'a' + filetype
        if os.path.isfile(name):
            os.remove(name)
        if os.path.isfile('a.html'):
            os.remove('a.html')

    # 解析文件
    def parse(self):
        logging.info('----------------开始解析----------------')
        if self.filetype == '.pdf' or self.filetype == '.PDF':
            logging.info('开始解析pdf:%s' %self.filename)
            html = pdftostr.pdftohtml(self.filedata)
            # 不使用pdfminer
            # try:
            #     text = pdftostr.pdftostr(self.filedata)
            # except:
            #     logging.info('未生成text')
            #     self.delete_file()
            #     return '', html
            # else:
            #     # 成功把pdf文件转化为text文本，并把text返回
            #     logging.info('生成text、html成功')
            #     self.delete_file()
            #     return text, html
            self.delete_file()
            status = 'HH'
            return html, html, status
        elif self.filetype == '.docx' or self.filetype == '.DOCX':
            logging.info('开始解析docx:%s' %self.filename)
            docxfile = StringIO.StringIO()
            docxfile.write(self.filedata)
            # 成功把docx文件转化为text文本
            text = docx2txt.process(docxfile)
            self.create_file()
            html = office_convert.convert(self.filetype)
            logging.info('生成text、html成功')
            self.delete_file()
            status = 'TH'
            return text, html, status
        elif self.filetype == '.doc' or self.filetype == '.DOC':
            # 因为使用catdoc把doc解析为str是出现乱码，所以使用html做为text的返回参数
            logging.info('开始解析doc:%s' %self.filename)
            # text = doc2str.doc2str(self.filedata)
            self.create_file()
            realtype = magic.from_file('a.doc',mime=True)
            if realtype == 'application/msword':
                try:
                    html = office_convert.convert(self.filetype)
                except:
                    status = 'XX'
                    return '','',status
                self.delete_file()
                logging.info('生成html成功')
                status = 'HH'
                return html, html, status
            else:
                logging.warning('不是真正的doc文件')
                status = 'XX'
                return '', '', status
        elif self.filetype == '.xls' or self.filetype == 'XLS':
            logging.info('开始解析xls:%s' %self.filename)
            self.create_file()
            html = office_convert.convert(self.filetype)
            try:
                text = xls2str.xls2str(self.filedata)
            except:
                logging.info('未生成text')
                self.delete_file()
                status = 'XH'
                return '', html, status
            else:
                logging.info('生成text、html成功')
                self.delete_file()
                status = 'TH'
                return text, html, status
        elif self.filetype == '.xlsx' or self.filetype == '.XLSX':
            logging.info('开始解析xlsx:%s' %self.filename)
            self.create_file()
            html = office_convert.convert(self.filetype)
            text = xlsx2str.xlsx2str(self.filedata)
            logging.info('生成text、html成功')
            self.delete_file()
            status = 'TH'
            return text, html,status
        elif self.filetype == '.ppt' or self.filetype == 'PPT':
            logging.info('开始解析ppt:%s' %self.filename)
            self.create_file()
            html = office_convert.convert(self.filetype)
            parsed = parser.from_file('a.ppt')
            text = parsed['content']
            logging.info('生成text、html成功')
            self.delete_file()
            status = 'TH'
            return text, html,status
        elif self.filetype == '.pptx' or self.filetype == 'PPTX':
            logging.info('开始解析pptx:%s' %self.filename)
            self.create_file()
            html = office_convert.convert(self.filetype)
            parsed = parser.from_file('a.pptx')
            text = parsed['content']
            logging.info('生成text、html成功')
            self.delete_file()
            status = 'TH'
            return text, html,status
        elif self.filetype == '.txt' or self.filetype == '.TXT':
            logging.info('开始解析txt:%s' %self.filename)
            # text = self.filedata
            # if isinstance(text, str):
            #     coding = chardet.detect(text)['encoding']
            #     logging.info('编码类型：%s' % coding)
            #     if coding == 'GB2312':
            # 	    text1 = unicode(text, 'GB18030').encode('utf-8')
            #     else:
            # 		text1 = text
            # else:
            # 	text1 = text
            # return text1, text1
            name = 'a' + self.filetype
            xfile = open(name, 'wb')
            text = self.filedata
            try:
                # text1 = unicode(text, 'GB18030').encode('utf-8')
                text1 = text.decode('GB18030', 'ignore').encode('utf-8')
            except:
                status = "解析失败"
                return '', '', status
            xfile.write(text1)
            xfile.close()
            logging.info('生成原始文件')
            contents = open('a.txt', "r")
            f = open("a.html", "w")
            for lines in contents.readlines():
                f.write("<pre>" + lines + "</pre> \n")
            f.close()
            f1 = open("a.html", "r")
            html = f1.read()
            status = "解析成功"
            self.delete_file()
            return html, html, status
        elif self.filetype == '.html' or self.filetype == '.HTML':
            logging.info('开始解析html:%s' % self.filename)
            text = self.filedata
            if isinstance(text, str):
                coding = chardet.detect(text)['encoding']
                logging.info('编码类型：%s' % coding)
                if coding == 'GB2312':
            	    text1 = unicode(text, 'GBK').encode('utf-8')
                else:
            		text1 = text
            else:
            	text1 = text
            status = 'TH'
            return text1, text1, status
        elif self.filetype == '.xml' or self.filetype == '.XML':
            logging.info('开始解析xml:%s' % self.filename)
            text = self.filedata
            if isinstance(text, str):
                coding = chardet.detect(text)['encoding']
                logging.info('编码类型：%s' % coding)
                if coding == 'GB2312':
                    text1 = unicode(text, 'GBK').encode('utf-8')
                else:
                    text1 = text
            else:
                text1 = text
            status = 'TH'
            return text1, text1, status
        elif self.filetype == '.md' or self.filetype == '.MD':
            logging.info('开始解析md:%s' % self.filename)
            text = self.filedata
            if isinstance(text, str):
                coding = chardet.detect(text)['encoding']
                logging.info('编码类型：%s' % coding)
                if coding == 'GB2312':
            	    text1 = unicode(text, 'GBK').encode('utf-8')
                else:
            		text1 = text
            else:
            	text1 = text
            status = 'TH'
            return text1, text1, status
        else:
            status = '非'
            return '', '', status




#tika解析
        # def file2str(self,filedata,filename):
        #     os.chdir('/home/zxjd/Web/cace')
        #     filetype = os.path.splitext(filename)[1]
        #     x_file = open(filename, 'wb')
        #     x_file.write(filedata )
        #     x_file.close()
        #     parsed = parser.from_file(filename)
        #     text = parsed['content']
        #     if filetype == '.pdf':
        #         html = pdftostr.pdftohtml(filedata)
        #     else:
        #         html = ''
        #     return text, html




