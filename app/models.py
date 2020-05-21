from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

medallas_users = db.Table('medallas_users',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                            db.Column('medalla_id', db.Integer, db.ForeignKey('medalla.id'), nullable=False),
                            db.PrimaryKeyConstraint('user_id', 'medalla_id'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    logros = db.relationship('Logro', backref='user', lazy='dynamic')
    medallas = db.relationship('Medalla', secondary=medallas_users, backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def medallas_count(self):
        return db.session.query(Medalla).with_parent(self, "medallas").count()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Logro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64))
    descripcion = db.Column(db.String(240))
    casi_logro = db.Column(db.Boolean())
    logrado = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Logro {}>'.format(self.nombre)


class Medalla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64))
    descripcion = db.Column(db.String(240))

    def __repr__(self):
        return '<Medalla {}>'.format(self.nombre)
