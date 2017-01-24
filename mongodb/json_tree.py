import os
import json
def path_to_dict(path):
    d = {'text': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [
        path_to_dict(os.path.join(path,x)) 
        for x in os.listdir(path)
        	if os.path.isdir(os.path.join(path,x))
        ]
    else:
        d['type'] = "file"
    return d
print json.dumps(path_to_dict('/home/zxjd/zxjd_Project/'))

path_to_dict()