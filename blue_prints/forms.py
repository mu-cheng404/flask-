import wtforms
from wtforms.validators import Email,Length,EqualTo
from models import User_model,EmailCaptchaModel
from exts import db

#验证前端的表单是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=3,max=20,message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="密码不匹配")])

    #自定义验证 邮箱是否已经被注册 验证码是否正确
    def validate_email(self,filed):
        email = filed.data
        user = User_model.query.filter_by(email = email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册")

    def validate_captcha(self,filed):
        captcha = filed.data
        email = self.email.data
        emailCaptcha = EmailCaptchaModel.query.filter_by(email = email, captcha = captcha).first()
        if not emailCaptcha:
            raise wtforms.ValidationError(message="验证码错误")
        else:
            db.session.delete(emailCaptcha)
            db.session.commit()

#登录的表单验证
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])

#问答的表单验证
class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=6,max=100,message="标题不能为空！")])
    content = wtforms.StringField(validators=[Length(min=6,max=500,message="内容字数不符！")])

#答案的表单验证
class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=6,max=500,message="内容字数不符！")])
    question_id = wtforms.IntegerField()

#搜索的表单验证
class SearchForm(wtforms.Form):
    q = wtforms.StringField(validators=[Length(min=2,max = 100,message="输入格式错误！")])
