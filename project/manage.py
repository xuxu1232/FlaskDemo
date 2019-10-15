### 实现python manage.py runserver
### 实现python manage.py migrate

### 需要将models和views导入

import sys
from main import app,db
from views import *
from models import *
from flask_script import Manager
manager = Manager(app)


@manager.command
def migrate():
    db.create_all()
if __name__ == '__main__':
    manager.run()
#
# command = sys.argv[1]
# # python manage.py runserver ip:port
if sys.argv[1] == 'runserver' and sys.argv[2]:
    ip = sys.argv[2].split(':')[0]
    port = sys.argv[2].split(':')[1]
    app.run(host=ip,port=int(port))
# elif command == 'runserver': ## python manage.py runserver
#     app.run()
# elif command == 'migrate': ## python manage.py migrate
#     db.create_all()




