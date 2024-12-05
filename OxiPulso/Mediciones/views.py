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

from OxiPulso.funciones import init_mqtt, wait_for_message
from OxiPulso import app, db
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Iniciar MQTT
topic = os.environ.get('MQTT_TOPIC')
mqtt_client = init_mqtt(app, topic)


mediciones = Blueprint('mediciones', __name__)


@mediciones.route('/mediciones', methods=['GET', 'POST'])
def medicion():
    return render_template("mediciones/mediciones.html")

@mediciones.route('/tutorial')
def tutorial():
    return render_template("mediciones/tutorial.html")

@app.route('/mediciones/medir', methods=['POST'])
def publish_message():
    request_data = request.form['message']
    print(request_data)
    publish_result = mqtt_client.publish(topic, request_data)
    print(publish_result)
    
    # Espera a que se publique el valor medido
    measured_value = wait_for_message()
    # measured_value = {"HR":51,"SPO2":90}
    # measured_value = None
    
    if measured_value is not None:
        
        if "error" in measured_value:
            print(measured_value)
            return jsonify(success=False, error=measured_value["error"])
        
        print(measured_value)
        
        usuario_id = session.get('usuario_id')
        if usuario_id:
            try:
                nueva_medicion = Mediciones(
                    usuario_id=usuario_id,
                    bpm=measured_value["HR"],
                    spo2=measured_value["SPO2"],
                    fecha=datetime.today().strftime("%Y-%m-%d"),
                    hora=datetime.now().strftime("%H:%M:%S")
                )
                
                db.session.add(nueva_medicion)
                db.session.commit()
           
            except Exception as e:
               
                db.session.rollback()
                return jsonify(success=False, error="Error inesperado al guardar la medición")
        
        return jsonify(success=True, hr=measured_value["HR"], spo2=measured_value["SPO2"])
    else:
        return jsonify(success=False, error="No se recibió el valor del sensor a tiempo")
    
@mediciones.route('/historial')
def historial():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        mediciones = Mediciones.obtener_datos(id=usuario_id)
        # print(mediciones)
        return render_template("mediciones/historial.html", mediciones=mediciones)
        # return render_template("mediciones/historial.html")
    else:
        return redirect(url_for('usuarios.iniciarSesion'))
    
@mediciones.route('/mediciones/historial/datos')
def historial_obtener_datos():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        mediciones = Mediciones.obtener_datos(id=usuario_id)
        #return render_template("mediciones/historial.html", mediciones=mediciones)
        return jsonify(success=True, mediciones=mediciones)
    else:
        return redirect(url_for('usuarios.iniciarSesion'))
    

@mediciones.route('/mediciones/descargar')
def descargar():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        return Mediciones.descargar_csv(usuario_id)
    else:
        return jsonify(success=False, error="No se ha iniciado sesión")
    

@mediciones.route('/mediciones/resumen')
def resumen():   
    return render_template("mediciones/resumen.html")
    
    