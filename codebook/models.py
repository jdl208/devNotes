from codebook import login_manager, mongo, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(username):
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return None
    return User(user['username'], user['email'], user['password'],
                user['profile_pic'])


class User():
    def __init__(self, username, email, password, profile_pic):
        self.username = username
        self.email = email
        self.password = password
        self.profile_pic = profile_pic

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'email': self.email}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            email = s.loads(token)['email']
        except Exception:
            return None
        return mongo.db.users.find_one({'email': email})


class Post():
    def __init__(self, title, short_desc, content, author, date_posted, public, avatar):
        self.title = title
        self.short_desc = short_desc
        self.content = content
        self.author = author
        self.date_posted = date_posted
        self.public = public
        self.avatar = avatar
