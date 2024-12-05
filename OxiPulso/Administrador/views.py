from flask import (
    render_template,
    Blueprint,
    request,
    jsonify,
    session,
    redirect,
    url_for 
)
from OxiPulso.Mediciones.models import Mediciones
from OxiPulso.Autenticacion.models import Usuario
from .estadisticas import basicos
from dotenv import load_dotenv
import os

administrador = Blueprint('administrador', __name__)

load_dotenv()

USER_ADMIN = os.getenv('USER_ADMIN')
PASSWORD_ADMIN = os.getenv('PASSWORD_ADMIN')

@administrador.route('/administrador')
def inicio():
    return render_template("administrador/admonvista.html")

@administrador.route('/adminlogout')
def cerrarSesion():
    session['admin'] = None
    
    return redirect(url_for('administrador.inicio'))


@administrador.route('/administrador/login', methods=['GET', 'POST'])
def iniciarSesion():
    
    session.clear()
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('contraseña')
        
        if not usuario:
            return render_template("administrador/login.html", alert='Ingrese el usuario')
        if not password:
            return render_template("administrador/login.html", alert='Ingrese la contraseña')
        print(usuario, password)
        print(USER_ADMIN, PASSWORD_ADMIN)
        if usuario == USER_ADMIN and password == PASSWORD_ADMIN:
            session['admin'] = 1
            return redirect(url_for('administrador.inicio'))
        else:
            return render_template("administrador/login.html", alert='Usuario o contraseña incorrectos')
    return render_template("administrador/login.html")


@administrador.route('/administrador/usuarios')
def obtener_usuarios():
    usuarios = Usuario.obtener_datos_admon()  
    return jsonify(success=True, usuarios=usuarios)

@administrador.route('/administrador/mediciones', methods=['GET', 'POST'])
def obtener_mediciones():
    if request.method == 'POST':
        user = request.form.get('usuario')
        usuario = Usuario.query.filter_by(usuario=user).first()
        usuario_id = usuario.id
        print(usuario_id)
        mediciones = Mediciones.obtener_datos(id=usuario_id)
        return jsonify(success=True, mediciones=mediciones)
    else:
        print("hola")
        mediciones = Mediciones.obtener_datos_admon() 
        return jsonify(success=True, mediciones=mediciones)
    
@administrador.route('/admon/mediciones_vista')
def mediciones_vista():
    return render_template("administrador/mediciones.html")

@administrador.route('/admon/usuarios_vista')
def usuarios_vista():
    return render_template("administrador/usuarios.html")

@administrador.route('/administrador/descarga/mediciones')
def descargar_datos_medicion():
    return Mediciones.descargar_csv_all()
    

@administrador.route('/administrador/descarga/usuarios')
def descargar_datos_usuarios():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        #return render_template("mediciones/historial.html", mediciones=mediciones)
        return Usuario.descargar_csv(id=usuario_id)
    else:
        return Usuario.descargar_csv_all()    
    
@administrador.route('/administrador/estadisticas')
def estadisticas():
    (
        bpm_max_data,
        bpm_min_data,
        spo2_max_data,
        spo2_min_data,
        timeline_base64,
        barras_base64,
    ) = basicos()

    return render_template(
        'administrador/estadisticas.html',
        bpm_max_data=bpm_max_data,
        bpm_min_data=bpm_min_data,
        spo2_max_data=spo2_max_data,
        spo2_min_data=spo2_min_data,
         timeline_base64=timeline_base64,
        barras_base64=barras_base64
    )
    
@administrador.route('/administrador/all_mediciones')
def all_mediciones():
    mediciones = Mediciones.obtener_todos_datos()
    return jsonify(success=True, mediciones=mediciones)

@administrador.route('/administrador/descargar_datos_usuario/<int:id>')
def descargar_datos_usuario(id):
    return Mediciones.descargar_csv(id)