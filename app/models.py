# -*- coding: utf-8 -*-


from . import db, loginmanager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.SmallInteger, default=ROLE_USER)
    invoices = db.relationship('Invoice', backref = 'user',lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % self.username
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self,):
        return self.role_id == ROLE_ADMIN


class Invoice(db.Model):
    __tablename__ = 'invoices'
    number = db.Column(db.String(30), primary_key=True)
    cost = db.Column(db.Numeric(10.2))
    attached_cost = db.Column(db.Numeric(10.2))
    date = db.Column(db.Date)
    check_code = db.Column(db.String(30))
    upload_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    filename = db.Column(db.String(128))
    code = db.Column(db.String(30))

    def __repr__(self):
        return '<Invoice %r>' % self.number


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(20), unique=True)
    users = db.relationship('User',backref = 'department')

    def __repr__(self):
        return '<Department %r>' % self.id


@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def load_department():
    return [(d.id , d.department_name) for d in Department.query.order_by(Department.id).all()]