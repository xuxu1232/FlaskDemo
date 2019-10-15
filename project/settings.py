import os
### 第一种写法
SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost/flask'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True ## 请求结束后自动提交
SQLALCHEMY_RTACK_MODIFICATIONS = True ### 跟踪修改 flask1.x版本之后的配置项
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True


## 第二种写法
class Product:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  ## 请求结束后自动提交
    SQLALCHEMY_RTACK_MODIFICATIONS = True  ### 跟踪修改 flask1.x版本之后的配置项
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Config(Product):
    ## 正式环境的配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost/flask'




BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class TestConfig(Product):
    ## 测试环境的配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'test.db')
    DEBUG = True

    ## 用于session加密
    SECRET_KEY = "ertdesytcut5wsyttiersftudtriuyft=="


STATIC_PATH = os.path.join(BASE_DIR,'static')