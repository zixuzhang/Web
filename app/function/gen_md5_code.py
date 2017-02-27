import random, string, hashlib

def gen_md5_code(author, tag):
    md5 = hashlib.md5()
    md5.update(author)
    md5.update(tag)
    share_hash = md5.hexdigest()
    chars = string.letters + string.digits
    share_code = ''.join([random.choice(chars) for i in range(4)])
    return  share_hash, share_code