# -*- coding: utf-8 -*-
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import *
import re, os, StringIO, subprocess,logging,commands

os.chdir('/home/zxjd/Web/cace')
def pdftostr(data):
    fp = StringIO.StringIO()
    fp.write(data)
    #fp = open(u'6-成果转化.项目可行性报告.pdf', 'rb')
    pdfstr = u''
    #创建一个PDF文档解析器对象
    parser = PDFParser(fp)
    #创建一个PDF文档对象存储文档结构
    #提供密码初始化，没有就不用传该参数
    #document = PDFDocument(parser, password)
    document = PDFDocument(parser)
    #检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    #创建一个PDF资源管理器对象来存储共享资源
    #caching = False不缓存
    rsrcmgr = PDFResourceManager(caching = False)
    # 创建一个PDF设备对象
    laparams = LAParams()
    # 创建一个PDF页面聚合对象
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    #创建一个PDF解析器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    #处理文档当中的每个页面

    # doc.get_pages() 获取page列表
    #for i, page in enumerate(document.get_pages()):
    #PDFPage.create_pages(document) 获取page列表的另一种方式
    replace=re.compile(r'\s+')
    # 循环遍历列表，每次处理一个page的内容
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout=device.get_result()
        # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
        # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
        for x in layout:
            #如果x是水平文本对象的话
            if(isinstance(x,LTTextBoxHorizontal)):
                text=re.sub(replace,'',x.get_text())
                if len(text)!=0:
                    #print text
                    pdfstr = pdfstr + text
                    #print pdfstr
    return pdfstr

def pdftohtml(data):
    os.chdir('/home/zxjd/Web/cace')
    name = 'a.pdf'
    pdf_file = open(name, 'wb')
    pdf_file.write(data)
    pdf_file.close()
    # str1 = "docker run -ti --rm -v ~/Web/cace:/pdf bwits/pdf2htmlex pdf2htmlEX --zoom 1.3 %s" % name
    # os.system(str1)
    # os.system("docker run -ti --rm -v ~/Web/cace:/pdf bwits/pdf2htmlex-alpine pdf2htmlEX --zoom 1.3 a.pdf")

    # a = os.popen("pdf2htmlEX a.pdf > a.html")
    # subprocess.call('docker run -ti --rm -v ~/Web/cace:/pdf bwits/pdf2htmlex pdf2htmlEX --zoom 1.3 a.pdf', shell=True)
    # subprocess.call(['docker', 'run', '-ti', '--rm', '-v', '~/Web/cace:/pdf', 'bwits/pdf2htmlex', 'pdf2htmlEX', '--zoom', '1.3', 'a.pdf'])
    # subprocess.call("pdf2htmlEX a.pdf", shell=True)
    # os.system("pdf2html --zoom 1.3 a.pdf")

    logging.info("开始命令行")
    a, b = commands.getstatusoutput('docker run -i --rm -v ~/Web/cace:/pdf bwits/pdf2htmlex pdf2htmlEX --zoom 1.3 a.pdf')
    logging.info(a)
    logging.info("b:" + b)
    if os.path.isfile('a.html'):
        logging.info('生成html成功')
    else:
        logging.warning('生成html失败')
    logging.info('开始读取html')
    file_html = open('a.html', 'r')

    html_data = file_html.read()
    file_html.close()
    return html_data