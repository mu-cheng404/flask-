from flask import Blueprint, render_template, request,g,redirect,url_for
from .forms import QuestionForm, AnswerForm, SearchForm
from models import QuestionModel,AnswerModel
from exts import db
from decorators import login_required
bp = Blueprint("qa",__name__, url_prefix="/")

@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html",questions = questions)

@bp.route("/qa/public_question",methods=["GET","POST"])
@login_required
def public_question():
    if(request.method == "GET"):
        return render_template('public_question.html')
    else:
        #接受问题的数据
        form = request.form
        form = QuestionForm(form) #验证器处理
        if(form.validate()):
            title = form.title.data
            content = form.content.data
            author_id = g.user.id
            question = QuestionModel(title=title, content=content, author_id=author_id)
            db.session.add(question)
            db.session.commit()
            #todo 跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question",form=form))


@bp.route("/qa/search",methods=["GET","POST"])
def search():
    print(request.form.get("q"))
    form = SearchForm(request.form)
    if form.validate():#验证通过
        print("验证通过")
        q = form.q.data
        questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
        return render_template("index.html",questions = questions)
    else:
        print(form.errors,form.q)
        return redirect(url_for("qa.index"))
@bp.route("/qa/qa_detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html",question = question)

@bp.route("/qa/public_answer",methods = ["GET","POST"])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))




