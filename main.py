from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/newpost')
        if not user:
            flash('User does not exist')
        if user.password != password:
            flash('Password is incorrect')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])


@app.route('/blog', methods=['POST', 'GET'])
def display():
    blogs = Blog.query.all()
    if request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('individual.html', blog=blog)
    else:
        return render_template('mainBlogPage.html', title="Blog Page", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def add_post():

    #owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']

        title_error = None
        body_error = None

        if len(title) == 0:
            title_error = 'Title cannot be blank'
        
        if len(body) == 0:
            body_error = 'Body cannot be blank'

        if title_error or body_error:
            return render_template('newpost.html', title_error=title_error, body_error=body_error, keeptitle=title, keepbody=body)

        else:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            #blog = Blog.query.filter_by(title=title, body=body).first()
            blog_id = new_post.id
            return redirect('/blog?id={0}'.format(blog_id))

    else:
        return render_template('newpost.html', title="New Blog")


if __name__ == '__main__':
    app.run()