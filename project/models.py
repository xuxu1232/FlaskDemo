from main import db
from datetime import datetime


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

class User(BaseModel):
    __tablename__ = 'user'
    name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    password = db.Column(db.String(32))
    identity = db.Column(db.String(32),nullable=True)
    age = db.Column(db.Integer, nullable=True)
    time = db.Column(db.DATETIME, default=datetime.now())
    term = db.Column(db.String(32),nullable=True)
    phone = db.Column(db.String(11),nullable=True)
    photo = db.Column(db.String(100),nullable=True)
    sex = db.Column(db.Integer,nullable=True,)

class Leave(BaseModel):
    __tablename__ = 'leave'

    #   审核中 0
    #   通过  1
    #   驳回  2
    #   销假  3
    leave_id = db.Column(db.Integer)
    leave_name = db.Column(db.String(32))  ## 姓名
    leave_type = db.Column(db.String(32))  ## 请假类型
    leave_start = db.Column(db.DATETIME) ##请假开始时间
    leave_end = db.Column(db.DATETIME) ## 请假结束时间
    leave_description = db.Column(db.TEXT)  ### 请假描述
    leave_phone= db.Column(db.String(11)) ## 请假人手机号
    leave_status = db.Column(db.Integer)  ## 请假状态
    leave_days = db.Column(db.Integer)  ## 请假天数

