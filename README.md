# OxiPulso

**Proyecto Final de Curso de la asignatura Sistemas de Comunicación II**

OxiPulso es una aplicación de monitoreo de signos vitales que permite medir la frecuencia cardíaca (bpm) y el nivel de saturación de oxígeno en sangre (SpO2) utilizando un sensor MAX30102 y un dispositivo ESP32. Los datos son enviados a un servidor mediante MQTT, donde se procesan y se muestran en una interfaz web.

Este proyecto fue desarrollado en la **Universidad Nacional de Ingeniería** como parte del proyecto final del curso de Sistemas de Comunicación II.

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Componentes y Conexiones](#componentes-y-conexiones)
- [Requisitos](#requisitos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso](#uso)
- [Créditos](#créditos)

---

## Descripción

Este proyecto forma parte de la asignatura Sistemas de Comunicación II y tiene como objetivo demostrar el uso de comunicación inalámbrica y protocolos de transmisión de datos en tiempo real para el monitoreo de salud. La aplicación permite visualizar en tiempo real los valores de frecuencia cardíaca y SpO2 desde cualquier dispositivo con acceso a internet.

---

## Características

- **Monitoreo en Tiempo Real**: Mide y transmite en tiempo real la frecuencia cardíaca y el nivel de SpO2.
- **Detección Automática de Dedo**: Notifica si el dedo no está correctamente posicionado en el sensor.
- **Interfaz Web**: Visualiza los datos en una interfaz web simple.
- **Conexión MQTT**: Comunicación entre el dispositivo y el servidor mediante MQTT.
- **Indicadores Visuales y Sonoros**:
  - LEDs para estado de conexión y envío de datos.
  - Buzzer para alertas de envío de datos.

---

## Componentes y Conexiones

### Componentes

1. **ESP32**: Microcontrolador principal.
2. **Sensor MAX30102**: Para medir frecuencia cardíaca y SpO2.
3. **3 LEDs**: Indicadores de estado.
4. **3 Resistencias de 220 Ω**: Para limitar la corriente en los LEDs.
5. **Buzzer**: Para notificaciones sonoras.

### Conexiones

#### Pines de LEDs y Buzzer:
- **LED indicando conexión a internet y broker**: `GPIO 13`
- **LED indicando datos enviados al broker**: `GPIO 12`
- **LED indicando desconexión de internet**: `GPIO 14`
- **Buzzer para indicar envío de datos**: `GPIO 16`

#### Pines del Sensor MAX30102:
- **SDA (Datos)**: Conectar al pin SDA del ESP32.
- **SCL (Reloj)**: Conectar al pin SCL del ESP32.
- **VCC (Alimentación)**: Conectar a 3.3V del ESP32.
- **GND (Tierra)**: Conectar a GND del ESP32.

## Requisitos

### Hardware

- **ESP32**: Microcontrolador para gestionar las mediciones y el envío de datos.
- **Sensor MAX30102**: Sensor de pulso y oxígeno en sangre.
- **3 LEDs y 3 resistencias de 220 Ω**: Indicadores visuales.
- **Buzzer**: Alerta sonora.
- **Cables de Conexión**: Para conectar el sensor y componentes al ESP32.

### Software

- Python 3.8+
- Flask
- MQTT Broker (ej. Mosquitto o EMQX)

---

## Instalación y Configuración

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tu_usuario/OxiPulso.git
    cd OxiPulso
    ```

2. **Instalar las dependencias**:
    Asegúrate de tener `Python` y `pip` instalados. Luego, ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configurar las variables de entorno**:
    Crea un archivo `.env` en la raíz del proyecto y configura las siguientes variables:
    ```plaintext
    DATABASE_URI=
    SECRET_KEY=
    MQTT_TOPIC=
    MQTT_BROKER_URL=
    MQTT_BROKER_PORT=
    MQTT_USERNAME=
    MQTT_PASSWORD=
    MQTT_KEEPALIVE=
    MQTT_TLS_ENABLE=
    USER_ADMIN=admin
    PASSWORD_ADMIN=
    ```

4. **Cargar el firmware en el ESP32**:
    Usa el IDE de Arduino o PlatformIO para cargar el código en el ESP32. Asegúrate de configurar correctamente los pines según el esquema de conexión.

5. **Ejecutar la aplicación en local**:
    ```bash
    flask run
    ```

---

## Uso

1. **Iniciar Sesión**:
   Accede a la página de inicio de sesión en la URL proporcionada y autentícate con las credenciales preconfiguradas.

2. **Realizar una Medición**:
   Una vez autenticado, sigue las instrucciones en pantalla para comenzar una medición. El ESP32 enviará los valores a través de MQTT, y los resultados se mostrarán en tiempo real en la interfaz web.

3. **Visualización de Datos**:
   La página principal muestra los resultados de frecuencia cardíaca y SpO2. Si el dedo no está posicionado en el sensor, se notificará en la interfaz.

---

## Créditos

Este proyecto fue desarrollado como parte del curso de **Sistemas de Comunicación II** en la Universidad Nacional de Ingeniería por:

- **Manuel Conrado**
- **Dylan Rizo**
- **Laura Portocarrero**

**Asesorado por**: Prof. Bayardo Solis
