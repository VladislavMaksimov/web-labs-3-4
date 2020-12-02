from flask import Flask, session, render_template, redirect, request, url_for
from entities import User
from storage import Storage

# Создаём приложение
app = Flask(__name__)

# Конфигурируем
# Устанавливаем ключ, необходимый для шифрования куки сессии
app.secret_key = b'_5#y2L"F4Q8ziDec]/'


# Описываем основные маршруты и их обработчики

# Главная страница
@app.route('/')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        return render_template('pages/index.html', user=user)
    else:
        return redirect('/login')


# Страница с формой входа
@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect('/')
    return render_template('pages/login.html', page_title='Auth Example')


# Обработка формы входа
@app.route('/login', methods=['POST'])
def login_action():
    page_title = 'Вход / Auth Example'

    # Введённые данные получаем из тела запроса
    if not request.form['email']:
        return render_template('pages/login.html', page_title=page_title, error='Требуется ввести email')
    if not request.form['password']:
        return render_template('pages/login.html', page_title=page_title, error='Требуется ввести пароль')

    # Ищем пользователя в БД с таким email паролем
    user = Storage.get_user_by_email_and_password(request.form['email'], request.form['password'])

    # Неверный пароль
    if not user:
        return render_template('pages/login.html', page_title=page_title, error='Неверный пароль')

    # Сохраняем пользователя в сессии
    session['user_id'] = user.id

    # Перенаправляем на главную страницу
    return redirect(url_for('home'))


# Форма регистрации
@app.route('/registration', methods=['GET'])
def registration():
    return render_template('pages/registration.html', page_title='Регистрация / Auth Example')


# Обработка формы регистрации
@app.route('/registration', methods=['POST'])
def registration_action():
    page_title = 'Регистрация | Auth Example'
    error = None
    # Проверяем данные
    if not request.form['email']:
        error = 'Требуется ввести Email'
    if not request.form['password']:
        error = 'Требуется ввести пароль'
    if not request.form['password2']:
        error = 'Требуется ввести повтор пароля'
    if request.form['password'] != request.form['password2']:
        error = 'Пароли не совпадают'

    # В случае ошибки рендерим тот же шаблон, но с текстом ошибки
    if error:
        return render_template('pages/registration.html', page_title=page_title, error=error)

    # Добавляем пользователя
    Storage.add_user(User(None, request.form['email'], request.form['password']))

    # Делаем вид, что добавление всегда без ошибки
    # Перенаправляем на главную
    return redirect(url_for('home'))


# Выход пользователя
@app.route('/logout')
def logout():
    # Просто выкидываем его из сессии
    session.pop('user_id')
    return redirect(url_for('home'))

# Вкладка задач
@app.route('/tasks')
def tasks():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        return render_template('pages/tasks.html', user=user, tasks=[11,22,33,44,55, 66])
    else:
        return redirect('/login')

@app.route('/tasks', methods=['POST'])
def add_task():
    if "user_id" not in session:
        return redirect('/login')

    title = request.form['title'] 
    description = request.form['description']
    user = Storage.get_user_by_id(session["user_id"])

    return render_template('pages/tasks.html', user=user, tasks=[11,22,33,44,55,66,77])

if __name__ == '__main__':
    app.env = 'development'
    app.run(port=3000, host='0.0.0.0', debug=True)