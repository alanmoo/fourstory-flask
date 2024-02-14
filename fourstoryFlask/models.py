from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oauth_token = db.Column(db.String(200), unique=True, nullable=False)

def save_user_token(token):
    new_user = User(oauth_token=token)
    db.session.add(new_user)
    db.session.commit()

def find_user_by_token(token):
    return User.query.filter_by(oauth_token=token).first()