from flask_sqlalchemy import  SQLAlchemy

db=SQLAlchemy()    # 创建数据库模型实例
from. import user
def init_db_app(app):
    db.init_app(app)