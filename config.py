from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    DEBUG = True 
    TESTING = True
    
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL')
    MQTT_BROKER_POR = os.environ.get('MQTT_BROKER_PORT')
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')  
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')  
    MQTT_KEEPALIVE =  5  
    MQTT_TLS_ENABLE = False  

    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = os.environ.get('SECRET_KEY')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    
class ProductionConfig(Config):
    DEBUG = False
