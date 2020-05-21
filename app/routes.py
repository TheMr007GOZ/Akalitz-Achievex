from flask import render_template, flash, redirect, url_for
from app import app, db
from flask_login import login_required
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, LogroForm
from app.models import User, Logro, Medalla


def add_medalla(medalla):
    current_user.medallas.append(medalla)
    db.session.commit()
    flash('Nuevo medalla obtenida: {}'.format(medalla.nombre))

def check_medallas_to_add():
    cuenta_logros = current_user.logros.count()
    if cuenta_logros == 1:
        print("una medalla")
        add_medalla(Medalla.query.filter_by(nombre="Primer paso").first())
    if cuenta_logros == 10:
        print("diez medallas")
        add_medalla(Medalla.query.filter_by(nombre="Diez seguidos").first())
    if cuenta_logros == 25:
        print("25 medallas")
        add_medalla(Medalla.query.filter_by(nombre="5 x 5").first())
    if cuenta_logros == 50:
        print("50 medallas")
        add_medalla(Medalla.query.filter_by(nombre="L").first())


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html', title='Welcome')


@app.route('/home')
@login_required
def home():
    logros = current_user.logros
    # medallas = db.session.query(Medalla).with_parent(current_user, "medallas").count() # alternative query
    medallas = current_user.medallas_count()
    return render_template('home.html', title="Home", logros=logros, medallascount=medallas)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Felicidades novato, te has registrado en el sistema')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/nuevo_logro', methods=['GET', 'POST'])
@login_required
def nuevo_logro():
    form = LogroForm()
    if form.validate_on_submit():
        logro = Logro(nombre=form.nombre.data, descripcion=form.descripcion.data, user=current_user)
        db.session.add(logro)
        db.session.commit()
        flash('Nuevo logro creado: {}'.format(logro.nombre))
        check_medallas_to_add()
        return redirect(url_for('home'))
    return render_template('nuevo_logro.html', title='Nuevo logro', form=form)


@app.route('/logros')
@login_required
def logros():
    logros = current_user.logros
    return render_template('logros.html', title='Lista de logros', logros=logros)


@app.route('/medallas')
def medallas():
    medallas_disponibles = Medalla.query.all()
    medallas_conseguidas = current_user.medallas
    return render_template('medallas.html', title='Lista de medallas', medallas=medallas_conseguidas, medallas_disponibles=medallas_disponibles)

@app.route('/rules', methods=['GET', 'POST'])
def rules():
    return render_template('rules.html', title='Reglas')