from flask import Flask, render_template, request, redirect, session, flash
from flask_bootstrap import Bootstrap
from database import db, User, Task
from datetime import timedelta
from datetime import datetime
import bcrypt
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(app)
bootstrap = Bootstrap(app)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('userName')
        password = request.form.get('password')
        existUser = User.query.filter_by(username=username).first()
        if existUser:
            flash('そのユーザー名は既に存在しています。別のユーザー名を選択してください。', 'error')
            return redirect('/signin')
        elif len(password) < 8 or len(password) > 16:
            flash('パスワードが短すぎるか長すぎます。8文字以上16文字以内で入力してください。', 'error')
            return redirect('/signin')
        elif not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
            flash('パスワードには数字と大文字を少なくとも1つ含めてください。', 'error')
            return redirect('/signin')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_post = User(username=username, password=hashed_password)

        db.session.add(new_post)
        db.session.commit()
        flash('ユーザー登録が完了しました。', 'success')
        return redirect('/')
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/signin', methods=['GET'])
def signinForm():
    return render_template('signin.html')


@app.route('/task', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("userName")
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.username == username and bcrypt.checkpw(password.encode('utf-8'), user.password):
            session['user_id'] = user.id
            return redirect('/home')
        else:
            flash('ユーザー名またはパスワードが間違っています。', 'error')
            return render_template('login.html')


@app.route('/home')
def showTask():
    if 'user_id' not in session:
        flash('セッションが切れました。','error')
        return redirect('/')
    user_id = session['user_id']
    user = db.session.get(User, user_id)
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.due.asc()).all()
    return render_template('task.html', user=user, tasks=tasks)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.clear()
    return redirect("/")


@app.route('/addTask', methods=['POST'])
def addTask():
    if (request.method == 'POST'):
        if 'user_id' not in session:
            flash('セッションが切れました。', 'error')
            return redirect('/')
        title = request.form.get('task')
        limit = request.form.get('deadline')
        limit = datetime.strptime(limit, '%Y-%m-%d')
        user_id = session['user_id']
        new_task = Task(title=title, due=limit, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/home')


@app.route('/doneTask',methods=['POST'])
def doneTask():
    if request.method=='POST':
        if 'user_id' not in session:
            flash('セッションが切れました。', 'error')
            return redirect('/')
        taskId = request.form.get('doneTaskId')
        task = Task.query.get(taskId)
        db.session.delete(task)
        db.session.commit()
        return redirect('/home')

@app.route('/editTask',methods=['POST'])
def editTask():
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('セッションが切れました。', 'error')
            return redirect('/')
        taskId = request.form.get('editTaskId')
        task = Task.query.get(taskId)
        task.title = request.form.get('editTaskTitle')
        task.due = datetime.strptime(request.form.get('editTaskLimit'), '%Y-%m-%d')
        db.session.commit()
        return redirect('/home')


if __name__ == "__main__":
    app.run()
