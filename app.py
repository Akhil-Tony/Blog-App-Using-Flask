# from email.policy import default
from flask import Flask, redirect, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class blog_post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    posted_by = db.Column(db.String(20),nullable=False) #,default='N/A'
    posted_on = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())

    def __repr__(self):
        return self.title
#db.create_all()
#db.session.commit()

@app.route('/')
def welcome():
    return render_template('index.html')
@app.route('/posts/new',methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']

        new_post = blog_post(title=post_title,content=post_content,
        posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

@app.route('/posts',methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']

        new_post = blog_post(title=post_title,content=post_content,
        posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = blog_post.query.order_by(blog_post.posted_on).all()
        return render_template('posts.html',posts=all_posts)

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    to_edit = blog_post.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.author = request.form['author']
        to_edit.content = request.form['post']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=to_edit)

@app.route('/posts/delete/<int:id>')
def delete(id):
    to_delete = blog_post.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/posts')

if __name__ == "__main__":
    app.run(debug=True)
