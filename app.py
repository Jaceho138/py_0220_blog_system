from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define UTC+8 timezone
UTC_PLUS_8 = timezone(timedelta(hours=8))


# Define Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Title
    content = db.Column(db.Text, nullable=False)  # Content
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC_PLUS_8))  # Creation time


# Create database tables
with app.app_context():
    db.create_all()


# Homepage route
@app.route('/')
def index():
    return render_template('index.html')


# Post list route
@app.route('/posts')
def posts():
    all_posts = Post.query.all()  # fetch all posts
    return render_template('post.html', posts=all_posts)


# create post route
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']  # Get title
        content = request.form['content']  # Get content
        new_post = Post(title=title, content=content)
        db.session.add(new_post)  # Add post
        db.session.commit()  # Commit changes
        return redirect(url_for('posts'))
    return render_template('create.html')


if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
