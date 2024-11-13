from OxiPulso import db
import pandas as pd
import os
from flask import send_file,jsonify

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fechaNacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    usuario = db.Column(db.String(50), nullable=False, unique=True)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(250), nullable=False)
    fechaRegistro = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, nombre, fechaNacimiento, sexo, usuario, correo, contraseña, fechaRegistro):
        self.nombre = nombre
        self.fechaNacimiento = fechaNacimiento
        self.sexo = sexo
        self.usuario = usuario
        self.correo = correo
        self.contraseña = contraseña
        self.fechaRegistro = fechaRegistro
    
    def __repr__(self):
        return f"Nombre: {self.nombre}\nUsuario: {self.usuario}\nCorreo: {self.correo}"

    def to_dict(self):
        return {
            'id': self.id,
            'sexo': self.sexo,
            'nombre': self.nombre,
            'correo': self.correo,
            'nacimiento': self.fechaNacimiento,

        }
    
    
    @classmethod
    def obtener_datos_admon(cls):
        datos = cls.query.all()
        datos_dict_admon = [dato.to_dict() for dato in datos]
        return datos_dict_admon
        
    @classmethod
    def descargar_csv(cls, usuario_id):
        usuario = cls.query.filter_by(id=usuario_id).first()
        
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        datos = [usuario.to_dict()]

        df = pd.DataFrame(datos)

        carpeta = 'OxiPulso/archivos'
        
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        ruta = os.path.join(carpeta, f"{usuario.nombre}.csv")

        df.to_csv(ruta, index=False)

        print("Se descargó")
        return send_file(ruta, as_attachment=True)
        
    @classmethod
    def descargar_csv_all(cls):
        datos = db.session.query(
            Usuario.id, 
            Usuario.nombre, 
            Usuario.fechaNacimiento, 
            Usuario.sexo, 
            Usuario.usuario, 
            Usuario.correo
        ).all()

        df = pd.DataFrame(datos, columns=['ID', 'Nombre', 'Fecha de Nacimiento', 'Sexo', 'Usuario', 'Correo'])

        base_dir = os.path.dirname(os.path.abspath(__file__))  # Base directory of the script
        carpeta = os.path.join(base_dir, 'archivos')
        
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Asegúrate de limpiar el nombre del archivo de caracteres especiales
        nombre_archivo = "todos_los_usuarios.csv".replace(" ", "_")
        ruta = os.path.join(carpeta, nombre_archivo)

        df.to_csv(ruta, index=False)
        
        print("Se descargó")
        return send_file(ruta, as_attachment=True)
    
    