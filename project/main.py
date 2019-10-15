from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
from datetime import datetime


pymysql.install_as_MySQLdb()
app = Flask(__name__)

## 连接数据库
## app.config:类字典
###BASE_DIR: E:\flask\FlaskDemo\project   当前文件，项目所在根目录 ,
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# print(BASE_DIR)
### 1.连接sqlite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR,'test.db')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True ## 请求结束后自动提交
# app.config['SQLALCHEMY_RTACK_MODIFICATIONS'] = True ### 跟踪修改 flask1.x版本之后的配置项
# # print(app.config['SQLALCHEMY_DATABASE_URI'])

### 2.连接mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost/flask'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True ## 请求结束后自动提交
# app.config['SQLALCHEMY_RTACK_MODIFICATIONS'] = True ### 跟踪修改 flask1.x版本之后的配置项
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['DEBUG'] = True



## 第一种
# app.config.from_pyfile('settings.py')## 使用python文件作为配置文件

# # # 第二种
app.config.from_object('settings.Product')
app.config.from_object('settings.TestConfig') ## 使用类作为配置
# app.config.from_object('settings.Config')
# app.config.from_envvar()## 环境变量中加载
# app.config.from_json()## 从json中加载
# app.config.from_mapping()### 字典类型


db = SQLAlchemy(app)  #绑定flask项目，db为创建的实例对象
