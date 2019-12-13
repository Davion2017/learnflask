from flask import Flask, render_template, request, url_for, redirect, session
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    content = {
        'questions': Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template("index.html", **content)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        account = request.form.get('account')
        password = request.form.get('password')
        user = User.query.filter(User.account == account, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'用户名或密码错误'


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template("regist.html")
    else:
        account = request.form.get('account')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 账号验证
        user = User.query.filter(User.account == account).first()
        if user:
            return u'账号已注册，请更换账号'
        else:
            if password1 != password2:
                return u'密码输入不等，请重新输入'
            else:
                user = User(account=account, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/', methods=['GET', 'POST'])
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer-content')
    answer = Answer(content=content)

    user_id = session['user_id']
    user = User.query.filter(user_id == User.id).first()
    answer.author = user
    print(user)

    question_id = request.form.get('question-id')
    question = Question.query.filter(question_id == Question.id).first()
    answer.question = question

    db.session.add(answer)
    db.session.commit()

    return render_template('detail.html', question=question)


@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q)))
    return render_template('index.html', questions=questions)


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
