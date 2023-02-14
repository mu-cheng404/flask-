from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session,g
from werkzeug.security import generate_password_hash,check_password_hash
from exts import mail
from flask_mail import Message
import string
import random
from exts import db
from models import EmailCaptchaModel,User_model
from .forms import RegisterForm, LoginForm


bp = Blueprint("auth",__name__,url_prefix="/auth")

@bp.route("/login",methods=['GET',"POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = User_model.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password,password):
                    #flask将session加密存入cookie,把cookie拿到服务端解密，找到这个ID
                    session['user_id'] = user.id
                    return redirect("/")
                else:
                    print("密码错误")
                    return "登录失败，密码错误"
            else:
                return "登录失败，您还未注册"
        else:
            return redirect(url_for("auth.login"))


@bp.route("/register",methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        #进行表单验证 使用flask-wtf将表单验证 这个逻辑也独立出去
        form = RegisterForm(request.form)
        print(form)

        if form.validate():
            #验证通过后创建心得User记录
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = User_model(email = email,username = username, password = generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.email.errors)
            print(form.captcha.errors)
            print(form.username.errors)
            print(form.password.errors)
            print(form.password_confirm.errors)
            return redirect(url_for("auth.register"))


@bp.route("/captcha/email",methods=['GET'])
def captcha_email():
    email = request.args.get("email")
    source = string.digits*4 #源字符串
    captcha = random.sample(source,4) #随机取四个 返回的是列表类型
    captcha = "".join(captcha)
    message = Message(subject="知了传课注册", recipients=[email], body=f"您的验证码是{captcha}")
    #I/O操作 比较耗时
    mail.send(message)

    #验证码保存至数据库
    emailCaptcha = EmailCaptchaModel(email = email, captcha = captcha)
    db.session.add(emailCaptcha)
    db.session.commit()

    return jsonify({"code": 200, "message":"","data":None})


@bp.route("/logout")
def logout():
    session["user_id"] = None
    return redirect("/")
