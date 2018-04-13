from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    #TODO - Display blogs and titles on main page
    blogs = Blog.query.all()
    return render_template('mainBlogPage.html', title="Blog Page", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def add_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()
        blogs = Blog.query.all()
        return render_template('mainBlogPage.html', title="Blog Page", blogs=blogs)
    
    else:
        return render_template('newpost.html', title="New Blog")


if __name__ == '__main__':
    app.run()