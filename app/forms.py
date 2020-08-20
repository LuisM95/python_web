from wtforms import Form, HiddenField
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField

from .models import User


#validando un campo con regla de negocios 
def codi_validator(form, field):
    if field.data == 'codi' or field.data == 'Codi':
        raise validators.ValidationError('El username no es permitido')

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Los bots no pueden crear usuarios!')

class LoginForm(Form):
    username= StringField('Username', [
        validators.length(min=4, max=50 , message='El username se encuentra fuera de rango')
    ])
    password= PasswordField('Password', [
        validators.Required(message='El password es requerido.')
    ])

class RegisterForm(Form):
    username = StringField('username',[
        validators.length(min=4, max= 50),
        codi_validator
    ])
    email = EmailField('Email',[
        validators.length(min=6, max=100),
        validators.Required(message='El email es requerido.'),
        validators.Email(message='Ingrese un Email valido.')
    ])
    password = PasswordField('Password',[
        validators.Required(message='El Password es requerido.'),
        validators.EqualTo('confirm_password', message='La Contrasena no coincide')
    ])
    confirm_password = PasswordField('Confirm Password')
    accept = BooleanField('',[
        validators.DataRequired()
    ])
    honeypot = HiddenField("",[length_honeypot])

    def validate_username(self, username):
        if User.get_by_username(username.data):
            raise validators.ValidationError('El username ya esta en uso!')

    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError('El email ya esta en uso!')

    def validate(self):
        #validacion con sobreescritura del metodo validate
        if not Form.validate(self):
            return False

        if len(self.password.data) < 3:
            self.password.errors.append('El password es muy corto')
            return False

        return True

class TaskForm(Form):
    title = StringField('Titulo',[
        validators.length(min=4, max=50, message='Titulo fuera de Rango'),
        validators.DataRequired('El Titulo es Requerido!')
    ])
    description = TextAreaField('Descripcion',[
        validators.DataRequired('Require de Descripcion')
    ], render_kw={'rows': 5})