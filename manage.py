import os
from app import create_app, db
from app.models import User, Nodes , Files
from flask_script import Manager, Shell

app = create_app(os.getenv('FLASk_CONFIG') or 'default')

# app = create_app(os.getenv('FLASk_CONFIG') or 'production')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Nodes=Nodes, Files=Files)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()