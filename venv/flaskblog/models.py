from flaskblog import db,app
from datetime import datetime
from flask_login import UserMixin
from flaskblog import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import secrets

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    img_file = db.Column(db.String,nullable=False, default='default.jpg')
    posts = db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self,expire=1800):
        s = Serializer(app.config['SECRET_KEY'],expire)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            None
        return User.query.get(int(user_id))


    def __repr__(self):
        return f'USER (email="{self.email}" username="{self.username}" img_file="{self.img_file}")'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text(150), nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f'POST (title="{self.title}" user_id="{self.user_id}" posted_on="{self.date_posted}"'
