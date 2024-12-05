from flask import (
   render_template,
   Blueprint,
   request,
   session,
   redirect,
   url_for 
)
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from OxiPulso import db
from OxiPulso.Autenticacion.models import Usuario

usuarios = Blueprint('usuarios', __name__)
administrador = Blueprint('administrador', __name__)
load_dotenv()


@usuarios.route('/registro', methods=['GET', 'POST'])
def registro():
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fechaNacimiento = datetime.strptime(request.form['fechaNacimiento'], '%Y-%m-%d').date()
        sexo = request.form.get('sexo')
        usuario = request.form.get('usuario')
        correo = request.form.get('email')
        contraseña = request.form.get('contraseña')
        confirmarContraseña = request.form.get('confirmarContraseña')

        # Verificaciones 
        if not nombre:
            return render_template("autenticacion/registro.html", alert = "Ingrese su nombre") 
        
        if not fechaNacimiento:
            return render_template("autenticacion/registro.html", alert = "Ingrese su fechaNacimiento") 
        
        if not sexo:
            return render_template("autenticacion/registro.html", alert = "Ingrese su sexo")
        
        if not usuario:
            return render_template("autenticacion/registro.html", alert = "Ingrese un usuario")
        
        if not correo:
            return render_template("autenticacion/registro.html", alert = "Ingrese un correo")
        
        if not contraseña:
            return render_template("autenticacion/registro.html", alert = "Ingrese una contraseña")
        
        if not confirmarContraseña:
            return render_template("autenticacion/registro.html", alert = "Repita la contraseña")

        if contraseña != confirmarContraseña:
            return render_template("autenticacion/registro.html", alert = "Las claves no coinciden")
        
        try:
            nuevoUsuario = Usuario(nombre, fechaNacimiento, sexo, usuario, correo, generate_password_hash(contraseña), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(nuevoUsuario)
            db.session.commit()
            
            
            session['usuario_id'] = nuevoUsuario.id
            
            db.session.close()
            return render_template("index.html", success = "Usuario registrado correctamente")
        
        except Exception as e:
            db.session.rollback()
            return render_template("autenticacion/registro.html", alert = "Usuario y/o correo ya existen")
        
    return render_template("autenticacion/registro.html")

@usuarios.route('/iniciarSesion', methods=['GET', 'POST'])
def iniciarSesion():
    session.clear()
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        if os.getenv("USER_ADMIN") == usuario and  os.getenv("PASSWORD_ADMIN") == request.form.get('contraseña'):
           return render_template("administrador/admonvista.html", success="Ha iniciado sesion como administrador")
        usuario = Usuario.query.filter_by(usuario = request.form.get('usuario')).first()
        # Verificariones
        if not request.form.get('usuario'):
            return render_template("autenticacion/iniciarSesion.html", alert = "Ingrese un usuario")
           
        if not request.form.get('contraseña'):
            return render_template("autenticacion/iniciarSesion.html", alert = "Ingrese una contraseña")
        
        
        if not usuario:
            return render_template("autenticacion/iniciarSesion.html", alert = "El usuario no existe")

    
        if not usuario or not check_password_hash(usuario.contraseña, request.form.get('contraseña')):
            return render_template('autenticacion/iniciarSesion.html', alert = "Contraseña invalida")
        
        elif os.getenv("USER_ADMIN") == usuario and os.getenv("PASSWORD_ADMIN") == request.form.get('contraseña'):
           return render_template("administrador/admon.html", alert = "Ingrese una contraseña")
        
        session['usuario_id'] = usuario.id
        
        return render_template('index.html', success="Ha iniciado sesion")
    
    return render_template("autenticacion/iniciarSesion.html")

@usuarios.route('/cerrarSesion')
def cerrarSesion():
    session['usuario_id'] = None
    return redirect(url_for('base.index'))


@administrador.route('/admonvista')
def admonvista():
    return render_template('administrador/admonvista.html')

