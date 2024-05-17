import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(80))
    penulis = db.Column(db.String(100))
    judul = db.Column(db.String(100))
    artikel = db.Column(db.String(200))

@app.route('/')
def index():
    files = Upload.query.order_by(desc(Upload.id)).all()
    return render_template('index.html', files=files)

@app.route('/show/<int:id>')
def show(id):
    file = Upload.query.filter_by(id=id).first()
    return render_template('show.html', file=file)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['file']
    upload = Upload(image = file.filename, artikel = request.form['artikel'], penulis = request.form['penulis'], judul = request.form['judul'])
    db.session.add(upload)
    db.session.commit()


    file.save(f'static/uploads/{file.filename}')
    
    return redirect('/')

if __name__ == '__main__':
    app.run()