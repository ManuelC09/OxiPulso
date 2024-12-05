#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <ArduinoJson.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"
#include "heartRate.h"

// WiFi
const char* ssid = "TIGO-BC0C";
const char* password = "4D99ED806883";
WiFiClient clienteESP32;

// MQTT
const char* mqtt_server = "broker.emqx.io";
const int mqtt_port = 1883; 
const char* client_id = "mqttx_a210389a"; 
const char* mqtt_user = "OxiPulso";  
const char* mqtt_password = "OxiPulso"; 

PubSubClient clienteMQTT(clienteESP32);

// Sensor MAX30105
MAX30105 sensorParticula;

uint32_t bufferIR[100]; // Datos del LED infrarrojo
uint32_t bufferRojo[100]; // Datos del LED rojo

int32_t longitudBuffer; // Longitud de datos
int32_t spo2; // Valor de SpO2
int8_t spo2Valido; // Indicador de validez de SpO2
int32_t frecuenciaCardiaca; // Valor de frecuencia cardíaca
int8_t frecuenciaCardiacaValida; // Indicador de validez de frecuencia cardíaca

// Pines de LEDs y buzzer
const int ledConexion = 13; // LED indicando conexión a internet y broker
const int ledEnvioDatos = 12; // LED indicando datos enviados al broker
const int ledDesconexion = 14; // LED indicando desconexión de internet
const int buzzerEnvioDatos = 16; // Buzzer para indicar envío de datos

// Variables para el proceso de medición
unsigned long tiempoInicio;
unsigned long tiempoActual;
const int duracionMedicion = 20000; // 20 segundos en milisegundos
const int intervaloMedicion = 1000; // Intervalo de medición en milisegundos
int sumaFrecuenciaCardiaca = 0;
int sumaSpo2 = 0;
int medicionesValidas = 0;
bool midiendo = false;

// Configura el tiempo "keep alive" para la conexión MQTT a 120 segundos
const int keepAliveMQTT = 120;
unsigned long ultimoIntentoReconectar = 0;

void iniciarWiFi() {
    Serial.print("Conectando a la red WiFi: ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);  
    }
    Serial.println("\nConexión WiFi establecida");
    Serial.print("Dirección IP: ");
    Serial.println(WiFi.localIP());

    // Enciende el LED de conexión
    digitalWrite(ledConexion, HIGH);
}

void recibirMensajeMQTT(char* topico, byte* payload, unsigned int longitud) {
    Serial.print("Mensaje recibido en el tópico [");
    Serial.print(topico);
    Serial.println("]");

    String mensaje = "";
    for (int i = 0; i < longitud; i++) {
        mensaje += (char)payload[i];
    }

    if (mensaje.equals("medir")) {
        midiendo = false;
        iniciarMedicion();
    }
}

void iniciarMQTT() {
    clienteMQTT.setServer(mqtt_server, mqtt_port);
    clienteMQTT.setCallback(recibirMensajeMQTT);
    clienteMQTT.setKeepAlive(keepAliveMQTT);
}

bool reconectarMQTT() {
    if (clienteMQTT.connect(client_id, mqtt_user, mqtt_password)) {
        Serial.println("Conexión con el broker MQTT exitosa");
        clienteMQTT.subscribe("OxiPulso/Datos");
        return true;
    } else {
        Serial.print("Fallo al conectar con el broker MQTT, código de error: ");
        Serial.print(clienteMQTT.state());
        Serial.println(". Reintentando en unos segundos...");
        return false;
    }
}

void iniciarSensor() {
    if (!sensorParticula.begin(Wire, I2C_SPEED_FAST)) {
        Serial.println("Error: MAX30105 no encontrado. Verifique la conexión del sensor.");
        while (1);
    }

    byte brilloLed = 50;
    byte promedioMuestras = 1;
    byte modoLed = 2;
    byte tasaMuestreo = 100;
    int anchoPulso = 69;
    int rangoADC = 4096;

    sensorParticula.setup(brilloLed, promedioMuestras, modoLed, tasaMuestreo, anchoPulso, rangoADC);
    Serial.println("Sensor MAX30105 inicializado correctamente");
}

bool detectarDedo() {
    int lecturasConsecutivas = 0;
    int totalLecturas = 1; // Número de lecturas para validar la presencia del dedo
    int umbralIR = 5000; // Umbral para la señal IR, ajusta según las pruebas

    for (int i = 0; i < totalLecturas; i++) {
        long valorIR = sensorParticula.getIR();
        if (valorIR > umbralIR) {
            lecturasConsecutivas++;
        }
        delay(100); // Pequeña pausa entre lecturas
    }

    bool dedoDetectado = (lecturasConsecutivas > (totalLecturas / 2));
    if (dedoDetectado) {
        Serial.println("Dedo detectado en el sensor.");
    } else {
        Serial.println("No se detectó dedo en el sensor.");
    }
    return dedoDetectado;
}

void recopilarDatosSensor() {
    longitudBuffer = 100;
    for (byte i = 0; i < longitudBuffer; i++) {
        while (!sensorParticula.available())
            sensorParticula.check();

        bufferRojo[i] = sensorParticula.getRed();
        bufferIR[i] = sensorParticula.getIR();
        sensorParticula.nextSample();
    }
}

void iniciarMedicion() {
    if (!midiendo) {
        Serial.println("Iniciando mediciones de frecuencia cardíaca y SpO2 durante 20 segundos...");
        tiempoInicio = millis();
        sumaFrecuenciaCardiaca = 0;
        sumaSpo2 = 0;
        medicionesValidas = 0;
        midiendo = true;
    }

    tiempoActual = millis();

    if (tiempoActual - tiempoInicio >= duracionMedicion) {
        midiendo = false;
        if (medicionesValidas > 0) {
            int frecuenciaPromedio = sumaFrecuenciaCardiaca / medicionesValidas;
            int spo2Promedio = sumaSpo2 / medicionesValidas;

            Serial.print("Medición completa. Frecuencia cardíaca promedio: ");
            Serial.println(frecuenciaPromedio);
            Serial.print("SpO2 promedio: ");
            Serial.println(spo2Promedio);

            enviarDatosMQTT(frecuenciaPromedio, spo2Promedio);
        } else {
            enviarErrorMQTTNoDedo();
        }
    } else if (tiempoActual - tiempoInicio >= medicionesValidas * intervaloMedicion) {
        if (!detectarDedo()) {
            enviarErrorMQTTNoDedo();
            midiendo = false;
            return;
        }

        recopilarDatosSensor();
        maxim_heart_rate_and_oxygen_saturation(bufferIR, longitudBuffer, bufferRojo, &spo2, &spo2Valido, &frecuenciaCardiaca, &frecuenciaCardiacaValida);

        if (frecuenciaCardiacaValida && spo2Valido) {
            if ((frecuenciaCardiaca > 40 && frecuenciaCardiaca < 100) && (spo2 > 60 && spo2 < 100)) {
                sumaFrecuenciaCardiaca += frecuenciaCardiaca;
                sumaSpo2 += spo2;
                medicionesValidas++;
            }
        }
    }
}

void enviarDatosMQTT(int frecuenciaCardiaca, int spo2) {
    StaticJsonDocument<200> doc;
    doc["HR"] = frecuenciaCardiaca;
    doc["SPO2"] = spo2;
    char bufferJson[512];
    serializeJson(doc, bufferJson);
    if (clienteMQTT.publish("OxiPulso/Datos", bufferJson)) {
        Serial.print("Datos enviados a MQTT: ");
        Serial.println(bufferJson);

        digitalWrite(ledEnvioDatos, HIGH);
        digitalWrite(buzzerEnvioDatos, HIGH);
        delay(1000);
        digitalWrite(buzzerEnvioDatos, LOW);
        digitalWrite(ledEnvioDatos, LOW);
    } else {
        Serial.println("Error al enviar datos a MQTT.");
    }
}

void enviarErrorMQTTNoDedo() {
    clienteMQTT.publish("OxiPulso/Datos", "{\"error\":\"No se detectó dedo\"}");
    Serial.println("Error: No se detectó dedo. Mensaje de error enviado a MQTT.");
}

void setup() {
    Serial.begin(115200);

    pinMode(ledConexion, OUTPUT);
    pinMode(ledEnvioDatos, OUTPUT);
    pinMode(ledDesconexion, OUTPUT);
    pinMode(buzzerEnvioDatos, OUTPUT);

    iniciarWiFi();
    iniciarMQTT();
    iniciarSensor();
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        digitalWrite(ledDesconexion, HIGH);
        iniciarWiFi();
    } else {
        digitalWrite(ledDesconexion, LOW);
    }

    if (!clienteMQTT.connected()) {
        unsigned long ahora = millis();
        if (ahora - ultimoIntentoReconectar > 5000) {
            ultimoIntentoReconectar = ahora;
            if (reconectarMQTT()) {
                ultimoIntentoReconectar = 0;
            }
        }
    } else {
        clienteMQTT.loop();
    }

    if (midiendo) {
        iniciarMedicion();
    }

    delay(100);
}
