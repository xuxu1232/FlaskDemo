from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
from datetime import datetime
from models import User


pymysql.install_as_MySQLdb()
app = Flask(__name__)

## 连接数据库
## app.config:类字典
###BASE_DIR: E:\flask\FlaskDemo\project   当前文件，项目所在根目录 ,
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# print(BASE_DIR)
### 1.连接sqlite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR,'test.db')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True ## 请求结束后自动提交
# app.config['SQLALCHEMY_RTACK_MODIFICATIONS'] = True ### 跟踪修改 flask1.x版本之后的配置项
# # print(app.config['SQLALCHEMY_DATABASE_URI'])

### 2.连接mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True ## 请求结束后自动提交
app.config['SQLALCHEMY_RTACK_MODIFICATIONS'] = True ### 跟踪修改 flask1.x版本之后的配置项
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True






## 创建模型
db = SQLAlchemy(app)  #绑定flask项目，db为创建的实例对象

## 封装（自定义）save,merge,delete方法
class BaseModel(db.Model):
    __abstract__ = True ## 声明抽象类，可以被继承，不会被重写
    id = db.Column(db.Integer,primary_key=True)
    def save(self):
        db.session.add(self)
        db.session.commit()
    def merge(self):
        db.session.merge(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserInfo(BaseModel):
    __tablename__ = 'userinfo'   ## 指定映射的表名
    # id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer,default=1)
    time = db.Column(db.DATETIME,default=datetime.now())





## 数据迁移
## create_all():修改模型属性，表结构不同步
            ####修改模型，同步表
            ####再次执行，表结构，不变，也不会报错
db.create_all() ## 同步表结构



## 操作
### 增加数据
#### 单条增加
# userinfo = UserInfo(name='张三',age=19)
# db.session.add(userinfo)
# db.session.commit()


## 增加多条
# db.session.add_all(
#     [
#         UserInfo(name='lisi',age = 11),
#         UserInfo(name='lisi',age = 11),
#         UserInfo(name='lisi',age = 11),
#         UserInfo(name='lisi',age = 11),
#         UserInfo(name='lisi',age = 11),
#     ]
# )
# db.session.commit()


## 查询
## all:返回所有数据，包含所有对象,一个列表
# data = UserInfo.query.all()
# for one in data:
#
#     print(one.name)

## get:只能通过id 进行查询,返回一个对象,如果没有结果，返回一个None
data = User.query.get(1)
print(data)

## filter/filter_by:返回符合条件的数据，一个列表
# data = UserInfo.query.filter_by(name='lisi').all()
# print(data)

# data = UserInfo.query.filter(UserInfo.name == 'lisi').all()
# print(data)

## first:返回符合条件的第一个对象,不能跟在all()后面
# data = UserInfo.query.filter(UserInfo.name == 'lisi').first()
# print(data)



## order_by:排序
# 升序(默认)
# 按照id进行升序
# data = UserInfo.query.order_by(UserInfo.id).all()
# print(data)
# data = UserInfo.query.order_by('id').all()

# 降序：desc
# 使用id进行降序
# data = UserInfo.query.order_by(UserInfo.id.desc()).all()
# print(data)
# data = UserInfo.query.order_by(db.desc("id")).all()
# print(data)


## 分页
## limit(2):取两条数据
## offset(2).limit(2):偏移两个，取两个
# data = UserInfo.query.limit(2).all()
# data = UserInfo.query.offset(2).limit(2).all()

## 修改
# data = UserInfo.query.filter(UserInfo.id==1).first()
# data.name = 'wangwu'
# db.session.merge(data)
# db.session.commit()


## 删除
## 第一种
# data = UserInfo.query.filter().first()
# print(data.id)
# db.session.delete(data)
# db.session.commit()

## 第二种
# data = UserInfo.query.filter(UserInfo.id == 2).delete()
# db.session.commit()

## 利用封装的方法进行操作增删改
## 增加
# user = UserInfo(name='awu',age=19)
# user.save()

## 修改
# user = UserInfo.query.get(13)
# user.name = 'aliu'
# user.merge()

## 删除
# user = UserInfo.query.get(5)
# user.delete()

@app.route('/')
def index():
    return 'ORM测试'

if __name__ == '__main__':
    app.run(port=8000,debug=True)