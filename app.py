from flask import Flask,session,g
import config #导入配置文件
from exts import db,mail
from models import User_model
from blue_prints.qa import bp as qa_bp
from blue_prints.auth import bp as auth_bp
from flask_migrate import Migrate

#项目初始化
app = Flask(__name__)
app.config.from_object(config) #加载所有配置到项目中
db.init_app(app) #将db对象与项目进行绑定
mail.init_app(app) #将mial与项目进行绑定
app.register_blueprint(qa_bp) #将蓝图与app进行绑定
app.register_blueprint(auth_bp)
migrate = Migrate(app,db) #视图迁移

@app.before_request
def _before_request():
    user_id = session.get("user_id")
    if user_id:
        print(f"钩子函数被触发，user_id为{user_id}")
        user = User_model.query.get(user_id)
        setattr(g,"user",user) #放入全局变量
    else:
        setattr(g,"user",None)

@app.context_processor
def _context_processor():
    return {"user":g.user}


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")