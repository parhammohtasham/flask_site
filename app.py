from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite'

db=SQLAlchemy(app)

class BlogPost(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.Text)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/posts')
def posts():
    posts=BlogPost.query.all()
    return render_template('posts.html',posts=posts)

@app.route('/add/post', methods=['GET','POST'])
def addpost():
    if request.method=='POST':
        post_title=request.form['title']
        post_body=request.form['body']
        blog_post=BlogPost(title=post_title,body=post_body)
        db.session.add(blog_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('addpost.html')
    
@app.route('/delete/post/<int:id>')
def deletepost(id):
    blog_post=BlogPost.query.get(id)
    db.session.delete(blog_post)
    db.session.commit()
    return redirect('/posts')

@app.route('/edit/post/<int:id>', methods=['POST','GET'])
def update(id):
    blog_post=BlogPost.query.get(id)
    if request.method=='POST':
        post_title=request.form['title']
        post_body=request.form['body']
        blog_post.title=post_title
        blog_post.body=post_body
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('editPost.html',post=blog_post)

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)