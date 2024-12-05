# __init__.py
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración de la APP
app.config.from_object('config.ProductionConfig')

# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Session(app)

db = SQLAlchemy(app)


# Registrar Blueprints
from OxiPulso.views import base
from OxiPulso.Autenticacion.views import usuarios
from OxiPulso.Mediciones.views import mediciones
from OxiPulso.Administrador.views import administrador

app.register_blueprint(usuarios)
app.register_blueprint(base)
app.register_blueprint(mediciones)
app.register_blueprint(administrador)


# Ejecutar todas las consultas
with app.app_context():
    db.create_all()
