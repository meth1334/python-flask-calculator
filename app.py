from flask import Flask, render_template, request, flash, redirect, url_for
import database
import os
from flask_login import LoginManager, login_user, login_required
from user_login import UserLogin

app = Flask(__name__)
connection = database.create_connection('localhost', 'goga', '23Vivatcadet', 'nginx')
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/')
@login_required
def main():
    return render_template('index.html' , records = database.read_info(connection), title = "Таблица"  )


@app.route('/post', methods = ['POST'])
def post():
    json = request.get_json(force=True)
    date = json['date']
    ip_addr = json['ip_addr']
    calculation = json['calculation']
    result = json['result']
    database.save_info(date, ip_addr, calculation, result, connection)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = database.get_user_by_login(request.form['login'], connection)
        print(user, request.form['psw'])
        if user and user[2] == request.form['psw']:
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('main'))
 
        flash("Неверная пара логин/пароль", "error")
 
    return render_template("login.html", title="Авторизация")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if  len(request.form['login']) > 3 \
            and len(request.form['psw']) > 3 and request.form['psw'] == request.form['psw2']:
            res = database.add_user(request.remote_addr, request.form['login'], request.form['psw'], connection)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Данный пользователь уже существует. Введите другой login", "error")
        else:
            flash("Неверно заполнены поля", "error")
    
 
    return render_template("register.html", title="Регистрация")

@login_manager.user_loader
def load_user(id):
    print("Загрузка пользователя")
    return UserLogin().fromDB(id, database, connection)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(host='127.0.0.1', port=5002)



