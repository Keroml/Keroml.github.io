from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fort_telecom2.db'
db = SQLAlchemy(app)

#После запуска нужно создать бд
#(лично как у  вас не знаю) в пайчарме открыть Python console и последовательно написать:
#from app import app, db
#app.app_context().push()
#db.create_all()
#дальше всё должно работать

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(300), nullable=False)
    lastname = db.Column(db.String(300), nullable=False)
    product = db.Column(db.String(300), nullable=False)
    criteria1 = db.Column(db.Integer, nullable=False)
    criteria2 = db.Column(db.Integer, nullable=False)
    criteria3 = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/review', methods=['POST',"GET"])
def review():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        product = request.form['product']
        criteria1 = request.form['criteria1']
        criteria2 = request.form['criteria2']
        criteria3 = request.form['criteria3']
        review = request.form['review']

        post = Review(firstname = firstname, lastname = lastname, product = product,criteria1 = criteria1, criteria2 = criteria2, criteria3 = criteria3 , review = review )

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/thanks')
        except:
            db.session.rollback()
            return "Произошла какая-то ошибка"
    else:
        return render_template('review.html')

@app.route('/thanks',methods=['POST',"GET"])
def thanks():
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template("thanks.html")

@app.route('/view_review', methods=['GET'])
def view_review():
    # Получаем параметры фильтрации и сортировки
    product_filter = request.args.get('product_filter', '')
    sort_by = request.args.get('sort_by', 'date_newest')
    
    # Базовый запрос
    query = Review.query
    
    # Применяем фильтр по продукту
    if product_filter:
        query = query.filter(Review.product == product_filter)
    
    # Применяем сортировку
    if sort_by == 'date_newest':
        query = query.order_by(Review.date_posted.desc())
    elif sort_by == 'date_oldest':
        query = query.order_by(Review.date_posted.asc())
    elif sort_by == 'rating_highest':
        query = query.order_by(
            ((Review.criteria1 + Review.criteria2 + Review.criteria3)/3).desc()
        )
    elif sort_by == 'rating_lowest':
        query = query.order_by(
            ((Review.criteria1 + Review.criteria2 + Review.criteria3)/3).asc()
        )
    
    posts = query.all()
    return render_template('view_review.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
