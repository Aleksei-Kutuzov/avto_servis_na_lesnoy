import datetime
import random
import sys
from DB_settings import *
import time
from Imports_module import *
with open("errors.log", "w") as log:
    log.write(f"###############################STARTED NEW TO {time.localtime().__repr__()}###############################\n")
def write_log(type, value, traceback):
    with open("errors.log", "w") as log:
        log.write(f"{datetime.time()} ->> {type}: {value} {traceback}\n")

sys.excepthook = write_log
sys.stdout = open('stdout.log', 'w')
if os.path.exists("Oauth_module_lv.py"):
    from Oauth_module_lv import *
elif os.path.exists("Oauth_module_hv.py"):
    from Oauth_module_hv import *
else:
    raise FileNotFoundError


SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
print(SQLALCHEMY_DATABASE_URI, "DB-URL")


import random, string
def randomword(length):
   letters = string.digits + "ABCDE"
   return ''.join(random.choice(letters) for i in range(length))

failed_sign_in = False
class reviews:
    def __init__(self, text, type_comment, user):
        self.user = user
        self.text = text
        self.type = type_comment


comments = [reviews("Привет", "standard", "Admin"), reviews("Ура работает", "comment", "Боб (не губка)"), reviews("Хей, Ёу ёУ оо", "standard", "Репер миша")]

app = Flask(__name__)
app.secret_key = "9160b3eeb2c35e810d578df7df855dd9fd61f8b7b0b71eee9cff3c674fbb9f81"
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\\Users\\Алексей\\Desktop\\avto_servis_na_lesnoy\\users.db'


db = SQLAlchemy(app)

class UnconfirmedUser(db.Model):
    __tablename__ = 'unconfirmed_users'
    id = db.Column(db.Text(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(255), nullable=False)
    password = db.Column(db.Text(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    host_key = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name[:10])

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Text(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(255), nullable=False)
    password = db.Column(db.Text(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name[:10])


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route("/")
@app.route("/index")
def index():
    print(session)
    return render_template("index.html", activePage=0, sessionIsTrue="name" in session)

@app.route("/about")
def about():
    return render_template("about.html", activePage=4, sessionIsTrue="name" in session)

@app.route("/services")
def services():
    return render_template("services.html", activePage=1, sessionIsTrue="name" in session)

@app.route("/reviews")
def reviews():
    return render_template("reviews_T.html", activePage=2, comments=comments, sessionIsTrue="name" in session)

@app.route("/logout")
def logout():
    print(session.values())
    session.clear()
    return redirect("/")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html", activePage=3, sessionIsTrue="name" in session)

@app.route("/login", methods=['POST', "GET"])
def login():
    global username, password
    global failed_sign_in
    print(failed_sign_in)
    message = ''
    print(request.method.title())
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        remember = request.form.get('customCheck1')  # Проверяем, был ли установлен флажок "Запомнить пароль"
        session["id"] = "__un__"
        session["name"] = "__un__"
        session["picture"] = "__un__"
        session["email"] = email
        print(session)
        global user
        user = User.query.filter_by(email=session["email"], password=password).first()

        # Проверка, что пользователь существует, прежде чем работать с ним
        if user:
            print("Вход " + user.name)  # Выводит имя пользователя
        else:
            print(f"Пользователь {session['id']} не найден")
            session.clear()
            failed_sign_in = True

    if failed_sign_in:
        failed_sign_in = False
        return render_template("login.html", activePage=5, sessionIsTrue="name" in session, failed_sign_in=[rf"Не удалось войти, вы можете зарегистрироваться ", "здесь"])

    return render_template("login.html", activePage=5, sessionIsTrue="name" in session, failed_sign_in=False)


@app.route("/registration", methods=['POST', "GET"])
def registration():
    global username, password, failed_sign_in
    print(request.method.title())
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        name = request.form['inputUserName']
        session["id"] = time.time()
        session["name"] = name
        session["picture"] = "__un__"
        session["email"] = email
        # if get_id_g(session["email"]):
        #     session["id"] = get_id_g(session["email"])
        print(session)
        global user
        if User.query.filter_by(name=session["name"]).first() or UnconfirmedUser.query.filter_by(name=session["name"]).first():
            print(type(str("2")))
            return render_template("login.html", activePage=5, sessionIsTrue="name" in session, failed_sign_in="Не удалось зарегистрироваться, в системе есть пользователь с данным именем")
        user = UnconfirmedUser(email=session["email"], password=password, id=session["id"], name=session["name"], login=session["email"], picture=session["picture"], host_key=str(randomword(16) + session["name"]))

        # Проверка, что пользователь существует, прежде чем работать с ним
        if user:
            print("Регистрация " + user.name + "    " + user.host_key)  # Выводит имя пользователя
            db.session.add(user)
            db.session.commit()
        else:
            print(f"Пользователь {session['id']} не зарегистрировался")
            session.clear()
            failed_sign_in = True

    if failed_sign_in:
        failed_sign_in = False
        return render_template("login.html", activePage=5, sessionIsTrue="name" in session, failed_sign_in=[rf"Не удалось зарегистрироваться, вы можете зарегистрироваться ", "здесь"])
    return render_template("registration.html", activePage=6, sessionIsTrue="name" in session)

@app.route("/login_g")
def login_g():
    print(session)
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)
    # return render_template("login.html", activePage=5)

@app.route("/loginwithgoogle")
def loginwithgoogle():
    print(session.values())
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session.clear()

    session["id"] = id_info.get("sub") + "g"
    session["name"] = id_info.get("name")
    session["picture"] = id_info.get("picture")
    session["email"] = id_info.get("email")
    print(session.values())
    print(id_info.get("name"), "@@@@@@@@@@@@")
    global user
    user = User.query.filter_by(id=session["id"]).first()

    # Проверка, что пользователь существует, прежде чем работать с ним
    if user:
        print("Вход " + user.name)  # Выводит имя пользователя
    else:
        print(f"Пользователь {session['id']} не найден")
        session.clear()
        global failed_sign_in
        failed_sign_in = True
    return redirect("/login")


@app.route("/loginwithyandex")
def loginwithyandex():
    # Идентификатор приложения - YANDEX_CLIENT_ID
    # Пароль приложения - YANDEX_CLIENT_SECRET
    # Адрес сервера Яндекс.OAuth
    baseurl = 'https://oauth.yandex.ru/'
    print(request.args.to_dict())
    if request.args.get('code', False):
        # Если скрипт был вызван с указанием параметра "code" в URL,
        # то выполняется запрос на получение токена
        data = {
            'grant_type': 'authorization_code',
            'code': request.args.get('code'),
            'client_id': YANDEX_CLIENT_ID,
            'client_secret': YANDEX_CLIENT_SECRET
        }
        response = requests.post(baseurl + "token", data=data)
        token_info = response.json()
        session.clear()
        # Получение информации о пользователе
        user_info = get_user_info(token_info["access_token"])

        # Сохранение информации о пользователе в сессии
        session["id"] = user_info.get("id") + "y"
        session["name"] = user_info.get("display_name")
        session["yandex_user_picture"] = user_info.get("default_avatar_id")
        session["email"] = user_info.get("default_email")
        session["picture"] = f'https://avatars.yandex.net/get-yapic/{session["yandex_user_picture"]}/islands-middle'
        print(session)
        print(session["name"])
        global user
        user = User.query.filter_by(id=session["id"]).first()

        # Проверка, что пользователь существует, прежде чем работать с ним
        if user:
            print("Вход " + user.name)  # Выводит имя пользователя
            return redirect("/index")
        else:
            print(f"Пользователь {session['id']} не найден")
            session.clear()
            global failed_sign_in
            failed_sign_in = True
            return redirect("/login")
    else:
        # Если скрипт был вызван без указания параметра "code",
        # то пользователь перенаправляется на страницу запроса доступа
        return redirect(baseurl + "authorize?response_type=code&client_id={}".format(YANDEX_CLIENT_ID))


def get_user_info(access_token):
    headers = {
        'Authorization': f'OAuth {access_token}'
    }
    user_info_response = requests.get('https://login.yandex.ru/info', headers=headers)
    return user_info_response.json()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
