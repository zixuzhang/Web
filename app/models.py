# coding=utf-8
from app import db, login_manage
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import random, string, hashlib, os, re, zipfile,chardet
from app.filedata_manage.filedata_manage import *
from app.file_parse.file_parse import File_Parse
from bson.objectid import ObjectId


class User(UserMixin, db.Document):
    __tablename__ = 'users'
    email = db.StringField(requeired=True)
    username = db.StringField(max_length=50)
    password_hash = db.StringField()
    confirmed = db.BooleanField()

    def get_id(self):
        return self.email

    @property
    def password(self):
        raise AttributeError('密码不是可读属性！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manage.user_loader
def load_user(user_id):
    return User.objects(email=user_id).first()


class Files(db.Document):
    filedata = db.FileField()
    filename = db.StringField()
    library = db.StringField()
    tag = db.ListField()
    library_md5 = db.StringField()
    author = db.EmailField()
    status = db.StringField()

    text = db.StringField()
    html = db.StringField()

    # 全文搜索
    def search(self,library,option,search_name):
        if search_name:
            # files = None
            if option == u'全文搜索':
                a = library
                if library == u'全部':
                    files = Files.objects(__raw__ = {"$or": [{'html': re.compile(search_name)}, {'filename': re.compile(search_name)}]})
                    files_list, count, match_count = fulltext_search1(files,search_name)
                    dict1 = {'files_list': files_list, 'count': count, 'match_count': match_count}
                    return dict1
                else:
                    files = Files.objects(__raw__ = {'library':library, "$or": [{'html': re.compile(search_name)}, {'filename': re.compile(search_name)}]})
                    files_list, count, match_count = fulltext_search1(files,search_name)
                    dict1 = {'files_list': files_list, 'count': count, 'match_count': match_count}
                    return dict1
            elif option == u'文件搜索':
                if library == u'全部':
                    files = Files.objects(__raw__={'filename': re.compile(search_name)})
                    files_list, count, match_count = filename_search(files)
                    dict1 = {'files_list': files_list, 'count': count, 'match_count': match_count}
                    return dict1
                else:
                    files = Files.objects(__raw__ = {'library':library,'filename': re.compile(search_name)})
                    files_list, count, match_count = filename_search(files)
                    dict1 = {'files_list': files_list, 'count': count, 'match_count':match_count}
                    return dict1


class Nodes(db.Document):
    node = db.ListField()
    parent_node = db.ListField()
    author = db.EmailField()
    share_status = db.BooleanField(default=False)
    share_md5 = db.StringField()
    share_code = db.StringField()
    share_node = db.StringField()

    #分享节点，生成share_md5 share_code share_node share_status 并存到数据库中
    def share(self):
        md5 = hashlib.md5()
        md5.update(self.author)
        self.share_node = '/'.join(self.node)
        md5.update(self.share_node)
        self.share_md5 = md5.hexdigest()
        chars = string.letters + string.digits
        self.share_code = ''.join([random.choice(chars) for i in range(4)])
        self.share_status = True
        self.save()
        return self.share_md5, self.share_code

    # 删除分享
    def delete_share(self):
        self.share_node = ''
        self.share_md5 = ''
        self.share_code = ''
        self.share_status = False
        self.save()

    # 删除节点
    def delete_node(self, node):
        nodes = Nodes.objects(author=self.author, node=node)
        for i in nodes:
            i.delete()
        nodes = Nodes.objects(author=self.author, parent_node=node)
        for i in nodes:
            i.delete()
        nodes = Nodes.objects(author=self.author, parent_node__all=node)
        for i in nodes:
            i.delete()
        files = Files.objects(author=self.author, tag__all=node)
        for i in files:
            i.delete()

    # 重命名节点
    def rename_node(self, node, rename, k):
        nodes = Nodes.objects(author=self.author, node=node)
        for i in nodes:
            i.node[k] = rename
            if i.share_status:
                i.share_node = '/'.join(i.node)
            i.save()
        nodes = Nodes.objects(author=self.author, parent_node=node)
        for i in nodes:
            i.node[k] = rename
            if i.share_status:
                i.share_node = '/'.join(i.node)
            i.parent_node[k] = rename
            i.save()
        nodes = Nodes.objects(author=self.author, parent_node__all=node)
        for i in nodes:
            if len(i.parent_node) > len(node):
                i.node[k] = rename
                if i.share_status:
                    i.share_node = '/'.join(i.node)
                i.parent_node[k] = rename
                i.save()
        files = Files.objects(author=self.author, tag__all=node)
        for i in files:
            i.tag[k] = rename
            if k == 0:
                i.library = rename
            i.save()

    # 新建节点
    def new_node(self, node, name, email):
        node1 = node[:]
        node1.append(name)
        Nodes(node=node1, parent_node = node, author = email).save()

class Manage():
    def upload(self, file, email, library_md5):
        filename = file.filename
        library_name = os.path.splitext(filename)[0]
        library = Nodes.objects(author=email, parent_node=[]).distinct('node')
        if library_name in library:
            return library_name + ' 已存在!'
        else:
            # 判断文件是否是zip类型
            if zipfile.is_zipfile(file):
                zf = zipfile.ZipFile(file, 'r')
                for name in zf.namelist():
                    # 多平台的兼容name1为Unicode
                    if isinstance(name, str):
                        if chardet.detect(name)['encoding'] == 'GB2312':
                            name1 = unicode(name, 'GBK').encode('utf-8')
                        else:
                            name1 = name
                    else:
                        name1 = name
                    # 使路径变为列表
                    c = name1.split('/')
                    # 根据name1判断是否为文件夹，是文件夹的话把目录信息存入Nodes表；
                    # 否则就可以判断出name是文件，然后把文件信息以及标签信息存入Files
                    if name1[-1] == '/':
                        node = c[:-1]
                        parent_node = c[:-2]
                        Nodes(node=node, parent_node=parent_node, author=email).save()
                    else:
                        filename = c[-1]
                        library = c[0]
                        tag = c[:-1]
                        data = zf.read(name)
                        #allowed_filetype = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
                        # file_parse = File_Parse(filename,data)
                        # text, html, status = file_parse.parse()
                        #把文件的元数据存储到FileMetadata数据库
                        Files(filedata=data, filename=filename, library=library, tag=tag, library_md5=library_md5,author=email).save()
                        # try:
                        #     Files(filedata=data, filename=filename, library=library, tag=tag, library_md5=library_md5,
                        #             text=text, html=html, status=status, author=email).save()
                        # except:
                        #     status = 'Toolarge'
                        #     Files(filedata=data, filename=filename, library=library, tag=tag, library_md5=library_md5,
                        #             status=status, author=email).save()
                return '上传成功！'