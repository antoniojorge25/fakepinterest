# criar os formularios do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmar = SubmitField('Fazer login')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email= email.data).first()
        if not Usuario:
            raise ValidationError('Usuário inexistente. Crie uma conta')


class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Nome de Usuario', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    corfirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_confirmar = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email= email.data).first()
        if Usuario:
            raise ValidationError('E-mail ja cadastrado. Faça login para continuar')
        

class FormFoto(FlaskForm):
    foto = FileField('foto', validators=[DataRequired()])
    botao_confirmar = SubmitField('Enviar')