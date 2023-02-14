#插件 避免循环应用问题
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


db = SQLAlchemy() #SQLAlchemy的一个实例对象，所有关于数据库的操作都通过这个对象 先创建对象但是不与app绑定
mail = Mail()