# criar rotas do site (links)
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Fotos
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename

@app.route('/', methods= ['GET','POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email= formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario= usuario.id))
    return render_template('homepage.html', form = formlogin)


@app.route('/criar-conta', methods= ['GET','POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data).decode('utf-8')
        usuario = Usuario(username= formcriarconta.username.data
                          ,email= formcriarconta.email.data
                          ,senha= senha)
        database.session.add(usuario)
        database.session.commit()
        logout_user()
        return redirect(url_for('perfil', id_usuario= usuario.id))
    return render_template('criar_conta.html', form = formcriarconta)

@app.route('/Perfil/<id_usuario>', methods= ['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], nome_seguro )
            arquivo.save(caminho)
            foto = Fotos(imagem= nome_seguro, id_usuario= current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html', usuario=current_user, form = formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form= None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos = Fotos.query.order_by(Fotos.data_criacao.desc()).all()
    return render_template('feed.html', fotos= fotos)
