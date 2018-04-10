from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import flask_sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.String(1000))

    def __init__(self, title, content):
        self.title = title
        self.content = content


if __name__ == '__main__':
    app.run()