from eng import *
from models import *
from re import match
from datetime import datetime

@app.errorhandler(404)
def page_not_found(error):
    return render_template('main.html'), 404

@app.route("/<page_name>/")
def main(page_name):
    return render_template(page_name+'.html')

@app.route("/")
def index():
    return render_template("main.html")
@app.route("/get-news/", methods=['GET'])
def get_news():
    news = db_session.query(News).all()

    data = [
    {"id": new.id,
     "title": new.title,
     "text": new.text,
     "date": new.date,
     "author": new.author.name}
    for new in news]

    return jsonify(data)

@app.route("/category/<string:category>/")
def get_category(category):
    categoryItem = db_session.query(Category).filter_by(name = category).first()
    news = db_session.query(News).filter_by(category_id = categoryItem.id).all()

    data = [
        {"id": new.id,
         "title": new.title,
         "text": new.text,
         "date": new.date,
         "author": new.author.name}
        for new in news]

    return render_template("categories.html", news=data)

@app.route("/news/<int:news_id>/")
def get_news_by_id(news_id):
    news_item = db_session.query(News).filter_by(id=news_id).first()
    comments = db_session.query(Comments).filter_by(news_id=news_id).all()
    if news_item:
        return render_template("news.html", news=news_item, comments=comments)
    else:
        return render_template("news.html", error="Новость не найдена")
    
@app.route('/add_comment/<int:news_id>', methods=['POST'])
def add_comment(news_id):
    if not current_user.is_authenticated:
        flash('Вы должны войти в систему, чтобы оставить комментарий.')
        return redirect(url_for('login'))

    comment_content = request.form.get('commentContent')
    if comment_content:
        new_comment = Comments(
            text=comment_content,
            date=datetime.now(),
            news_id=news_id,
            author_id=current_user.id
        )
        print('-'*20)
        print(new_comment)
        print('-'*20)
        db_session.add(new_comment)
        db_session.commit()
        flash('Комментарий добавлен.')
    else:
        flash('Комментарий не может быть пустым.')

    return redirect(url_for('get_news_by_id', news_id=news_id))

@app.route("/register/", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        login = request.form.get('username')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Проверка на совпадение паролей
        if password != confirm_password:
            error = 'Пароли не совпадают!'

        # Проверка на длину пароля
        elif len(password) < 8:
            error = 'Пароль должен содержать как минимум 8 символов!'

        # Проверка наличия заглавных и строчных букв, а также цифр в пароле
        elif not any(char.isupper() for char in password) or \
             not any(char.islower() for char in password) or \
             not any(char.isdigit() for char in password):
            error = 'Пароль должен содержать хотя бы одну заглавную букву, одну строчную букву и одну цифру!'

        # Проверка уникальности логина
        elif Author.query.filter_by(login=login).first():
            error = 'Такой логин уже существует!'

        # Проверка логина на соответствие критериям
        elif not match("^[a-zA-Z][a-zA-Z0-9]{3,15}$", login):
            error = 'Логин должен начинаться с буквы, состоять только из букв и цифр и иметь длину от 4 до 16 символов!'


        else:
            author = Author(name=nickname, login=login, password=password)
            db_session.add(author)
            db_session.commit()
            login_user(author)
            flash('Успешная регистрация!', 'success')
            return redirect(url_for('index'))  # Redirect to another page after successful registration
    return render_template('register.html', error=error)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        author = Author.query.filter_by(login=username).first()
        # Проверка ваших пользователей и паролей, например:
        if not author or not author.check_password(password):
            error = 'Неправильное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.'
        else:
            # Здесь вы можете добавить логику для входа пользователя, например, установить сеанс входа
            login_user(author)
            flash('Успешный вход!', 'success')
            return redirect(url_for('index')) 
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли!', 'success')
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('register'))
    return response

