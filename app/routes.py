# app/routes.py
from flask import render_template, request, redirect, url_for
from app import app
from app.models import Users, UserAlbums, Posts
from app import db
import uuid
from flask_login import current_user
# home page
@app.route("/")
def home():
    user_list = Users.query.all()
    return render_template("index.html", user_list=user_list)

# adds new users to the user list database
@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    username = request.form.get("username")
    email = request.form.get("email")
    new_user = Users(name=name, username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("home"))

# user profile page
@app.route("/userprofile/<int:user_id>", methods=["GET", "POST"])
def userprofile(user_id):
    user = Users.query.filter_by(id=user_id).first()
    album_list = UserAlbums.query.filter_by(user_id=user_id).all()
    post_list = Posts.query.filter_by(user_id=user_id).all()
    return render_template("userprofile.html", user=user, album_list=album_list, post_list=post_list)

# adds new albums to albums database
@app.route("/addalbum/<int:user_id>", methods=["POST"])
def addalbum(user_id):
    title = request.form.get("title")
    id=uuid.uuid4().hex
    user = Users.query.filter_by(id=user_id).first()
    new_album = UserAlbums(id=id,author=user, title=title)
    db.session.add(new_album)
    db.session.commit()
    return redirect(url_for("userprofile",user_id=user_id))
    
# adds new posts to post database
@app.route("/addpost/<int:user_id>", methods=["POST"])
def addpost(user_id):
    title = request.form.get("title")
    id=uuid.uuid4().hex
    user = Users.query.filter_by(id=user_id).first()
    new_post = Posts(id=id,author=user, title=title)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for("userprofile",user_id=user_id))

# updates current posts
@app.route("/update/<int:user_id>/<int:post_id>", methods=["GET", "POST"])
def update(user_id,post_id):
    post = Posts.query.filter_by(id=post_id).first()
    user = Users.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        newtitle = request.form.get("update_title")
        new_post = Posts(id=post_id, title=newtitle)
        db.session.add(new_post)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("userprofile",user_id=user_id))
    else:
        return render_template("update.html", post=post, user=user)

# deletes posts selected by user
@app.route("/delete/<int:user_id>", methods=["POST"])
def delete(user_id):
    user = Users.query.filter_by(id=user_id).first()
    post = Posts.query.filter_by(author=user).first()
    post.id = request.form.get('deletebox')
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("userprofile",user_id=user_id))

# deletes users
@app.route("/deleteuser/<int:user_id>", methods=["POST"])
def deleteuser(user_id):
    user = Users.query.filter_by(id=user_id).first()
    user.id = request.form.get('deletebox')
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))
