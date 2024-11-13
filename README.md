# OxiPulso

**Proyecto Final de Curso de la asignatura Sistemas de Comunicación II**

OxiPulso es una aplicación de monitoreo de signos vitales que permite medir la frecuencia cardíaca (bpm) y el nivel de saturación de oxígeno en sangre (SpO2) utilizando un sensor MAX30105 y un dispositivo ESP32. Los datos son enviados a un servidor mediante MQTT, donde se procesan y se muestran en una interfaz web.

Este proyecto fue desarrollado en la **Universidad Nacional de Ingeniería** como parte de los requisitos del curso de Sistemas de Comunicación II.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso](#uso)
- [Créditos](#créditos)

## Descripción

Este proyecto forma parte de la asignatura Sistemas de Comunicación II y tiene como objetivo demostrar el uso de comunicación inalámbrica y protocolos de transmisión de datos en tiempo real para el monitoreo de salud. La aplicación permite visualizar en tiempo real los valores de frecuencia cardíaca y SpO2 desde cualquier dispositivo con acceso a internet.

## Características

- **Monitoreo en Tiempo Real**: Mide y transmite en tiempo real la frecuencia cardíaca y el nivel de SpO2.
- **Detección Automática de Dedo**: Notifica si el dedo no está correctamente posicionado en el sensor.
- **Interfaz Web**: Visualiza los datos en una interfaz web simple.
- **Conexión MQTT**: Comunicación entre el dispositivo y el servidor mediante MQTT.

## Requisitos

### Hardware
- **ESP32**: Microcontrolador para gestionar las mediciones y el envío de datos.
- **Sensor MAX30105**: Sensor de pulso y oxígeno en sangre.
- **Cables de Conexión**: Para conectar el sensor al ESP32.

## Instalación y Configuración

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tu_usuario/OxiPulso.git
    cd OxiPulso
    ```

2. **Instalar las dependencias**:
    Asegúrate de que tienes `Python` y `pip` instalados. Luego, ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configurar las variables de entorno**:
    Crea un archivo `.env` en la raíz del proyecto y configura las siguientes variables:
    ```plaintext
    SECRET_KEY=tu_clave_secreta
    MQTT_BROKER_URL=broker.emqx.io
    MQTT_BROKER_PORT=1883
    ```

4. **Ejecutar la aplicación en local**:
    ```bash
    flask run
    ```

## Uso

1. **Iniciar Sesión**:
   Accede a la página de inicio de sesión en la URL proporcionada y autentícate con las credenciales preconfiguradas.

2. **Realizar una Medición**:
   Una vez autenticado, sigue las instrucciones en pantalla para comenzar una medición. El ESP32 enviará los valores a través de MQTT, y los resultados se mostrarán en tiempo real en la interfaz web.

3. **Visualización de Datos**:
   La página principal muestra los resultados de frecuencia cardíaca y SpO2. Si el dedo no está posicionado en el sensor, se notificará en la interfaz.

## Créditos

Este proyecto fue desarrollado como parte del curso de **Sistemas de Comunicación II** en la Universidad Nacional de Ingeniería por:

- **Manuel Conrado**
- **Dylan Rizo**
- **Laura Portocarrero**

**Asesorado por**: Prof. Bayardo Solis

