from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Używamy SQLite – baza tworzy się jako plik moja_baza.db w katalogu projektu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moja_baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definicja modelu ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

@app.route('/')
def index():
    # SELECT * FROM user;
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route('/me')
def about_me():
    return render_template("user.html", username="Mateusz Nadolski")

# UWAGA: nie tworzymy tabel automatycznie w trakcie importu!
# Tabele tworzymy ręcznie w terminalu, raz.
# Aby stworzyć tabele w bazie danych na podstawie modeli,
# musisz otworzyć terminal Pythona i wykonać: (plik migration_script.py)
# Zrób to tylko raz!

@app.route('/add/<int:num1>/<int:num2>')
def add(num1, num2):
    return f"Wynik to: {num1+num2}"


@app.route('/movies')
def my_movies():
    movies = [
    "Lord of the Rings",
    "Matrix",
    "Harry Potter",
    "Incredibles",
    "Monsters Inc."
    ]
    return render_template("movies.html", page_title='Moje ulubione filmy!!!', movies=movies)

@app.route('/form', methods = ["GET", "POST"])
def form():
    if request.method == 'GET':
        return render_template('form.html', message='')

    if request.method == "POST":
        message = request.form.get('message')
        return render_template('form.html', message=message)



if __name__ == '__main__':
    app.run(debug=True)
