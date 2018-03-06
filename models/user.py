import hashlib
from flask_login import AnonymousUserMixin, UserMixin


class User(UserMixin):
    username = None
    password = None

    def __init__(self, username, password=None):
        self.username = username
        if password:
            self.password = self.set_password(password)

    def set_password(self, password):
        return hashlib.md5(str(password).encode('utf-8')).hexdigest()

    def check_password(self, password):
        return hashlib.md5(password).hexdigest() == self.password

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.username)

    def __repr__(self):
        return '<User %r>' % self.username
