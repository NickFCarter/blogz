from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'b4308cvnh4e09z7jas'

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

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'list_blogs', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login', methods=['POST', 'GET'])
def login():
    username_error = None
    password_error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        if not user:
            username_error = "User does not exist"
            return render_template('login.html', username_error=username_error, username=username)
        if user and user.password != password:
            password_error = "Incorrect password"
            return render_template('login.html', password_error=password_error, username=username)
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_error = None
        password_error = None
        verify_error = None

        # TODO - validate user's data
        if (len(username) < 3):
            username_error = "Username must be at least 3 characters long"

        if (len(password) < 3):
            password_error = "Password must be at lest 3 characters long"

        if password != verify:
            verify_error = "Passwords do not match"

        if username_error or password_error or verify_error:
            return render_template('signup.html', username=username, username_error=username_error, password_error=password_error, verify_error=verify_error)

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            username_error = "Duplicate user"
            return render_template('signup.html', username_error=username_error, username=username)

    return render_template('signup.html')


@app.route('/blog', methods=['POST', 'GET'])
def list_blogs():
    blogs = Blog.query.all()
    if request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.filter_by(id=blog_id).first()
        user = User.query.filter_by(id=blog.owner_id).first()
        return render_template('individual.html', blog=blog, user=user)
    if request.args.get('user'):
        user_id = request.args.get('user')
        user = User.query.filter_by(id=user_id).first()
        user_blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('singleUser.html', user_blogs=user_blogs, user=user)
    else:
        return render_template('mainBlogPage.html', title="Blog Page", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def add_post():

    owner = User.query.filter_by(username=session['username']).first()

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
            new_post = Blog(title, body, owner)
            db.session.add(new_post)
            db.session.commit()
            blog = Blog.query.filter_by(title=title, body=body).first()
            blog_id = new_post.id
            return redirect('/blog?id={0}'.format(blog_id))

    else:
        return render_template('newpost.html', title="New Blog")


if __name__ == '__main__':
    app.run()