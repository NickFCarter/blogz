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
    return redirect('/blog')

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