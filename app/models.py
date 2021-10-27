#app/models.py

from app import db

# creates a database that contains the users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    
    def __repr__(self):
        return self.text

# creates a database that contains albums created by users
class UserAlbums(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    author = db.relationship(Users, backref=db.backref('albums', lazy=True))
    title = db.Column(db.Text())

    def __repr__(self):
        return f"<UserAlbums(id='{self.id}', user_id='{self.user_id}', title='{self.title}')>"

# creates a database that contains posts created by users
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    author = db.relationship(Users, backref=db.backref('posts', lazy=True))
    title = db.Column(db.Text())

    def __repr__(self):
        return f"<Posts(id='{self.id}', user_id='{self.user_id}', title='{self.title}')>"

# class Comments(db.Model):
#     # __tablename__ = 'albums'
#     id = db.Column(db.String(64), primary_key=True)
#     user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
#     author = db.relationship(Users, backref=db.backref('comments', lazy=True))
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
#     posts = db.relationship(Posts, backref=db.backref('comments', lazy=True))
#     # comments = db.relationship("Comment")

#     content = db.Column(db.Text())
#     # content = db.Column(db.Text())

#     def __repr__(self):
#         return f"<Comments(id='{self.id}', user_id='{self.user_id}', post_id='{self.post_id}', title='{self.title}')>"

