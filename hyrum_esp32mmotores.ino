#include "BluetoothSerial.h"
#include "math.h"

BluetoothSerial SerialBT;  // Instancia para comunicación Bluetooth


// Pines del primer BTS7960B (Motor 1)
#define RPWM1 18  // Pin RPWM del primer BTS7960B
#define LPWM1 19  // Pin LPWM del primer BTS7960B

// Pines del segundo BTS7960B (Motor 2)
#define RPWM2 17
#define LPWM2 16


// Pines del encoder del Motor 1
#define pinA 27  //A
#define pinB 26

// Pines del encoder del Motor 2
#define pinA2 33  //B
#define pinB2 32





volatile int contador1 = 0;


// Variables para el Motor 2
volatile int contador2 = 0;

unsigned long previousMillis1 = 0, previousMillis2 = 0, previousMillis3 = 0, previousMillis5 = 0, previousMillis8 = 0, previousMillis9 = 0;
unsigned long printMillis = 0;  // Temporizador para impresiones
long interval = 100;            // Intervalo de 100 ms

// Constantes para el cálculo de RPM
const int IMP = 11;   // Número de impulsos por revolución
const int Z_w = 200;  // Relación de engranajes

// Variables de odometría
float x = 0, y = 0, phi = PI / 2;  // Coordenadas y ángulo del robot
float deltaRd = 0, deltaRi = 0;    // Desplazamientos de las ruedas
const float R = 0.051;             // Radio de las ruedas
const float L = 0.252;             // Distancia entre ruedas
int cd1 = 0, ci1 = 0;              // Contadores anteriores

// Variables globales adicionales
volatile int contador1b = 0;  // Variable asociada al contador1
volatile int contador2b = 0;  // Variable asociada al contador2

float tiempo_muestreo;
float tiempo_muestreo3;

float tiempo_muestreo5;



float pv1_, cv3, cv3_, pv2_, cv4, cv4_, cv5_;
float sp1 = 0.00;
float pv1 = 0;
float Kp1 = 1.3, Ki1 = 0.5, Kd1 = 0.01;
float cv1 = 0.0, error1 = 0.0, error2 = 0.0, cv_prev = 0.0;


float sp2 = 0.00;
float pv2 = 0;
float Kp2 = 1.3, Ki2 = 0.5, Kd2 = 0.01;
float cv2 = 0.0, error12 = 0.0, error22 = 0.0, cv_prev2 = 0.0;


float sp5 = 0.00;
float pv5 = 0;
float Kp5 = 1.3, Ki5 = 0.5, Kd5 = 0.01;
float cv5 = 0.0, error15 = 0.0, error25 = 0.0, cv_prev5 = 0.0;


double hxd = 0.0;  // Primer valor: posición deseada en X
double hyd = 0.0;  // Segundo valor: posición deseada en Y

double controlTrayectoria = 0.0;
unsigned long previousMillisLED = 0;


bool ledState = LOW;
int s1, s2;

double u, w;
double u_;

// Estructura para devolver u y w
struct ControlOutput {
  double u;
  double w;
};

// Función para calcular u y w
ControlOutput calcularControl(double hxe, double hye, double phi, double K1, double K2, double a) {
  ControlOutput resultado;

  // Cálculo simplificado basado en qref2
  resultado.u = K1 * hxe * cos(phi) + K2 * hye * sin(phi);
  resultado.w = (K2 * hye * cos(phi) - K1 * hxe * sin(phi)) / a;

  return resultado;
}



double saturate(double value, double minValue, double maxValue) {
  if (value < minValue) return minValue;
  if (value > maxValue) return maxValue;
  return value;
}


float mapCustom(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

float pid1(float sp, float pv, float tiempo_muestreo) {
  float error = sp - pv;
  float cv = cv_prev + (Kp1 + Kd1 / tiempo_muestreo) * error
             + (-Kp1 + Ki1 * tiempo_muestreo - 2 * Kd1 / tiempo_muestreo) * error1
             + (Kd1 / tiempo_muestreo) * error2;
  cv = saturate(cv, -.16, .16);
  cv_prev = cv;
  error2 = error1;
  error1 = error;
  return cv;
}
float pid2(float sp, float pv, float tiempo_muestreo) {
  float error = sp - pv;
  float cv = cv_prev2 + (Kp2 + Kd2 / tiempo_muestreo) * error
             + (-Kp2 + Ki2 * tiempo_muestreo - 2 * Kd2 / tiempo_muestreo) * error2
             + (Kd2 / tiempo_muestreo) * error22;
  cv = saturate(cv, -.16, .16);
  cv_prev2 = cv;
  error22 = error12;
  error12 = error;
  return cv;
}

float pid5(float sp, float pv, float tiempo_muestreo) {
  float error = sp - pv;
  float cv = cv_prev5 + (Kp5 + Kd5 / tiempo_muestreo) * error
             + (-Kp5 + Ki5 * tiempo_muestreo - 2 * Kd5 / tiempo_muestreo) * error15
             + (Kd5 / tiempo_muestreo) * error25;
  cv = saturate(cv, -.16, .16);
  cv_prev5 = cv;
  error25 = error15;
  error15 = error;
  return cv;
}

String comando = "";  // Variable global para almacenar el comando recibido

String message = "";         // Variable para almacenar el mensaje completo
String boyluobGeneral = "";  // Almacena mensajes adicionales enviados cada 5 segundos
unsigned long lastTime = 0;  // Para almacenar el último tiempo registrado
int mensajeCounter = 0;      // Contador de mensajes enviados


// Variables globales para almacenar valores extraídos
float distanciaZ = 0.0;
float distanciaX = 0.0;
float distanciaY = 0.0;
float estado = 0.0;

// Variables para los indicadores
float valorA5 = 0.0;
float valorAE = 0.0;
float valorAS = 0.0;
float valorBS = 0.0;

float valorCE = 0.0;
float valorCS = 0.0;  // Nueva variable para CS
float valorCT = 0.0;  // Nueva variable para CT
float valorSA = 0.0;
float valorSB = 0.0;
float valorSC = 0.0;
float valorSP = 0.0;
float valorTL = 0.0;
float valorXA = 0.0;
float valorXB = 0.0;
float valorXD = 0.0;  // Nueva variable para XD
float valorYA = 0.0;
float valorYB = 0.0;
float valorYD = 0.0;  // Nueva variable para YD


void procesarMensaje(String mensaje) {
  mensaje.trim();  // Eliminar espacios extra al inicio o final del mensaje

  int start = 0;
  while (start < mensaje.length()) {
    String prefix = "";
    String valorNumerico = "";

    // Detectar prefijo de 1 o 2 caracteres (por ejemplo, 'A', 'AV', 'CB')
    if (isAlpha(mensaje[start])) {
      prefix += mensaje[start];
      if (start + 1 < mensaje.length() && isAlpha(mensaje[start + 1])) {
        prefix += mensaje[start + 1];
        start++;
      }
      start++;
    }


    // Extraer el valor numérico incluyendo signo negativo
    bool signoEncontrado = false;
    while (start < mensaje.length() && (isDigit(mensaje[start]) || mensaje[start] == '.' || (!signoEncontrado && mensaje[start] == '-'))) {
      if (mensaje[start] == '-') {
        signoEncontrado = true;  // Solo un signo negativo permitido al inicio
      }
      valorNumerico += mensaje[start];
      start++;
    }

    // Procesar según el prefijo

    // Procesar según el prefijo

    // Procesar según el prefijo





    // Procesar según el prefijo
    // Procesar según el prefijo
    if (valorNumerico.length() > 0) {
      if (prefix == "A") {
        Serial.print(" A " + valorNumerico);
      } else if (prefix == "A5") {
        Serial.print(" A5 " + valorNumerico);
        valorA5 = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "AE") {
        Serial.print(" AE " + valorNumerico);
        valorAE = valorNumerico.toFloat();  // Conversión a float
        //phi = 3.28;
        sp5 = phi - 1.57 + valorAE;
        // Ajuste directo al rango 0 a 2*pi
        sp5 = sp5 - (6.28 * floor(sp5 / 6.28));  // Módulo manual

        // Aseguramos que sea positivo
        if (sp5 < 0) {
          sp5 += 6.28;
        }
      } else if (prefix == "AS") {
        Serial.print(" AS " + valorNumerico);
        valorAS = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "BS") {
        Serial.print(" BS " + valorNumerico);
        valorBS = valorNumerico.toFloat();  // Conversión a float
      }



      else if (prefix == "CE") {

        Serial.print(" CE " + valorNumerico);
        valorCE = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "CS") {
        Serial.print(" CS " + valorNumerico);
        valorCS = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "CT") {
        Serial.print(" CT " + valorNumerico);
        valorCT = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "dx") {
        Serial.print(" dx " + valorNumerico);
        distanciaX = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "dy") {
        Serial.print(" dy " + valorNumerico);
        distanciaY = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "dz") {
        Serial.print(" dz " + valorNumerico);
        distanciaZ = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "g") {
        Serial.println(" g " + valorNumerico);
        estado = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "SA") {
        Serial.print(" SA " + valorNumerico);
        valorSA = valorNumerico.toFloat();  // Conversión a float
        s1 = valorSA;
      } else if (prefix == "SB") {
        Serial.print(" SB " + valorNumerico);
        valorSB = valorNumerico.toFloat();  // Conversión a float
        s2 = valorSB;
      } else if (prefix == "SC") {
        Serial.print(" SC " + valorNumerico);
        valorSC = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "SP") {
        Serial.print(" SP " + valorNumerico);
        valorSP = valorNumerico.toFloat();  // Conversión a float
        //phi = -(valorSP - 6.28);

        phi = valorSP;
      } else if (prefix == "TL") {
        Serial.print(" TL " + valorNumerico);
        valorTL = valorNumerico.toFloat();  // Conversión a float



        digitalWrite(4, !valorTL);
      } else if (prefix == "XA") {
        Serial.print(" XA " + valorNumerico);
        valorXA = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "XB") {
        Serial.print(" XB " + valorNumerico);
        valorXB = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "XD") {
        Serial.print(" XD " + valorNumerico);
        valorXD = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "YA") {
        Serial.print(" YA " + valorNumerico);
        valorYA = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "YB") {
        Serial.print(" YB " + valorNumerico);
        valorYB = valorNumerico.toFloat();  // Conversión a float
      } else if (prefix == "YD") {
        Serial.print(" YD " + valorNumerico);
        valorYD = valorNumerico.toFloat();  // Conversión a float
      } else {
        Serial.println("Prefijo no reconocido: " + String(prefix));
      }
    }
  }
}

void setup() {
  pinMode(12, OUTPUT);

  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);








  // Configurar pines del encoder y motores
  pinMode(pinA, INPUT);
  pinMode(pinB, INPUT);
  pinMode(pinA2, INPUT);
  pinMode(pinB2, INPUT);

  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  pinMode(RPWM2, OUTPUT);
  pinMode(LPWM2, OUTPUT);

  // Inicializar comunicación serie y Bluetooth
  Serial.begin(115200);  // Monitor serie
  Serial.println("Iniciando ESP32 para control de motores...");
  SerialBT.begin("ESP32-MotorControl2");  // Nombre del dispositivo Bluetooth
  SerialBT.println("Bluetooth iniciado. Envia valores en el formato: SP1,SP2 (ejemplo: 100,-255):");
  Serial.println("Bluetooth iniciado correctamente.");

  // Configurar interrupciones para los encoders
  attachInterrupt(digitalPinToInterrupt(pinA), interrupcion1, RISING);   // Flanco de subida en pinA (Motor 1)
  attachInterrupt(digitalPinToInterrupt(pinA2), interrupcion2, RISING);  // Flanco de subida en pinA2 (Motor 2)

  // Inicializar PWM en 0
  analogWrite(RPWM1, 0);
  analogWrite(LPWM1, 0);
  analogWrite(RPWM2, 0);
  analogWrite(LPWM2, 0);


  // Serial.println("Iniciando sensores...");
  // // Apagamos ambos sensores antes de inicializarlos
  // digitalWrite(XSHUT1, LOW);  // Apagamos el sensor 1
  // digitalWrite(XSHUT2, LOW);  // Apagamos el sensor 2
  // delay(50);

  // // Inicializamos el primer sensor
  // digitalWrite(XSHUT1, HIGH);  // Encendemos el sensor 1
  // delay(100);                  // Retraso más largo

  // if (!sensor1.begin()) {
  //   Serial.println(F("Error al iniciar el sensor 1. Verifica conexiones y alimentación."));
  //   while (1)
  //     ;  // Detenemos el programa si no se inicializa
  // }
  // sensor1.setAddress(0x30);  // Cambiamos la dirección del sensor 1 a 0x30


  // // Inicializamos el segundo sensor
  // digitalWrite(XSHUT2, HIGH);  // Encendemos el sensor 2
  // delay(100);                  // Retraso más largo

  // if (!sensor2.begin()) {
  //   Serial.println(F("Error al iniciar el sensor 2. Verifica conexiones y alimentación."));
  //   while (1)
  //     ;  // Detenemos el programa si no se inicializa
  // }
  // sensor2.setAddress(0x31);  // Cambiamos la dirección del sensor 2 a 0x31

  // Serial.println(F("Sensores listos"));
}
float error5 = 0;

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillisLED >= 100) {
    previousMillisLED = currentMillis;  // Actualiza el tiempo previo del LED
    ledState = !ledState;               // Alterna el estado del LED
    digitalWrite(12, ledState);
  }


  // digitalWrite(12, HIGH);
  // delay(50);  // Mantén el LED encendido por 1 segundo

  // // Apaga el LED (poniendo el pin en LOW)
  // digitalWrite(12, LOW);
  // delay(50);  // Mantén el LED apagado por 1 segundo
  //             // valorAS = .1;
  //             // valorBS = .1;






  if ((currentMillis - previousMillis1) >= interval) {
    //unsigned long currentMillis8 = millis();
    //SerialBT.println(tiempo_muestreo);
    previousMillis1 = currentMillis;
    // Inicia el cronómetro
    unsigned long startTime = millis();
    static unsigned long previousTime = 0;
    unsigned long currentTime = millis();
    tiempo_muestreo = (currentTime - previousTime) / 1000.0;
    previousTime = currentTime;
    Serial.println(tiempo_muestreo);


    pv1 = (1 / tiempo_muestreo) * contador1b * (60.0 / (IMP * Z_w));

    contador1b = 0;


    pv2 = (1 / tiempo_muestreo) * contador2b * (60.0 / (IMP * Z_w));  // Cálculo de velocidad para Motor 2




    contador2b = 0;


    sp1 = 0;
    sp2 = 0;
    if (valorAS != 0 || valorBS != 0) {

      sp1 = valorAS;
      sp2 = valorBS;
    }


    controlTrayectoria = valorCT;
    hxd = valorXD;



    hyd = valorYD;
    u = 0;
    w = 0;

    if (controlTrayectoria == 1) {

      float K1 = 0.2;  // Ganancia de control lineal
      float K2 = 0.2;  // Ganancia de control angular



      // Cálculo de hx y hy para la rueda derecha
      double hx = x + L * cos(phi);
      double hy = y + L * sin(phi);

      // Cálculo de hx y hy para la rueda izquierda (opuesto)
      double hx_opuesto = x - L * cos(phi);
      double hy_opuesto = y - L * sin(phi);

      // Cálculo de la posición del centro del robot
      double x_c = (hx + hx_opuesto) / 2;
      double y_c = (hy + hy_opuesto) / 2;

      // Cálculo de los errores en X y Y con respecto al centro
      double hxe = hxd - x_c;
      double hye = hyd - y_c;

      // Comprobar si las coordenadas actuales están dentro de la tolerancia
      if (abs(x_c - hxd) > 0.05 || abs(y_c - hyd) > 0.05) {



        ControlOutput control = calcularControl(hxe, hye, phi, K1, K2, L);


        // Desempaquetar los valores calculados
        u = control.u;
        w = control.w;
        u_ = u;
        //u = max(0.0, u);
        //  u=0;
        //  w= -.2;
        double w_d = (u + w * L) / (R);
        double w_i = (u - w * L) / (R);

        // Límites de las velocidades angulares
        double w_limit = 3.14;  // Límite máximo de velocidad angular (rad/s)

        w_d = saturate(w_d, -w_limit, w_limit);
        w_i = saturate(w_i, -w_limit, w_limit);
        // if (valorCE == 1) {


        //   static unsigned long previousTime5 = 0;
        //   unsigned long currentTime5 = millis();
        //   tiempo_muestreo5 = (currentTime5 - previousTime5) / 1000.0;
        //   previousTime5 = currentTime5;
        //   float pv5_ = sp5 * (3.14159 / 180.0);

        //   cv5 = pid5(sp5, phi, tiempo_muestreo5);
        //   cv5_ = mapCustom(cv5, -.23, .23, -255, 255);
        //   cv5_ = saturate(cv5_, -255, 255);

        //   w_d = w_d + (cv5_ * L) / R;
        //   w_i = w_i + (-cv5_ * L) / R;
        // }
        sp1 = w_d * R;
        sp2 = w_i * R;
      }
    }

    if (valorCE == 1) {


      static unsigned long previousTime5 = 0;
      unsigned long currentTime5 = millis();
      tiempo_muestreo5 = (currentTime5 - previousTime5) / 1000.0;
      previousTime5 = currentTime5;
      float pv5_ = sp5 * (3.14159 / 180.0);

      // cv5 = pid5(sp5, phi, tiempo_muestreo5);
      // cv5_ = mapCustom(cv5, -6.28, 6.28, -18.0, 18.0);
      // cv5_ = saturate(cv5_, -18.0, 18.0);
     error5 = sp5 - phi;

      // if (sp5 >= 0 && sp5 <= 1.57) {
      //   error5 = 6.28 + sp5 - phi;
      // }




      float w_d, w_i;
      
      if (error5 >= 0.15) {
        w_d = w_d + 0.5;  // Ajustado a 0.05
        w_i =  w_i - 0.5;  // Ajustado a 0.05
      } else if (error5 < -0.15) {
        w_d= w_d - 0.5;  // Ajustado a 0.05
        w_i = w_i + 0.5;  // Ajustado a 0.05
      } else if (error5 > -0.15 && error5 < 0.15) {
        w_d = w_d + 0;
        w_i = w_i + 0;
      }




      double w_limit = 4.51;  // Límite máximo de velocidad angular (rad/s)

      w_d = saturate(w_d, -w_limit, w_limit);
      w_i = saturate(w_i, -w_limit, w_limit);


      sp1 = sp1 + w_d * R;
      sp2 = sp2 + w_i * R;

sp1 = saturate(sp1, -.23, .23);
sp2 = saturate(sp2, -.23, .23);

    }
    if (valorCS == 1) {
      // Parámetros locales para distanciaX
      const int distanciaXMax = 160;                             // Rango máximo de distanciaX
      const float distanciaXMid = distanciaXMax / 2.0;           // Punto medio del rango
      const float distanciaXErrorMargin = 0.15 * distanciaXMid;  // Margen de error del 15%

      // Parámetros locales para distanciaZ
      const float distanciaZMax = 2.0;                           // Valor máximo de distanciaZ
      const float distanciaZMid = .50;                           // Referencia de mitad para distanciaZ
      const float distanciaZErrorMargin = 0.15 * distanciaZMid;  // Margen de error del 15%

      // Asignación de velocidad angular u (análogo a W)
      float w = 0.0;
      if (distanciaX >= distanciaXMid - distanciaXErrorMargin && distanciaX <= distanciaXMid + distanciaXErrorMargin) {
        w = 0;  // Dentro del margen de error
      } else if (distanciaX > distanciaXMid + distanciaXErrorMargin) {
        w = .1;  // Derecha del margen
      } else {
        w = -.1;  // Izquierda del margen
      }

      // Asignación para distanciaZ con signos invertidos w (análogo a U)
      float u = 0.0;
      if (distanciaZ >= distanciaZMid - distanciaZErrorMargin && distanciaZ <= distanciaZMid + distanciaZErrorMargin) {
        u = 0;  // Dentro del margen de error
      } else if (distanciaZ > distanciaZMid + distanciaZErrorMargin) {
        u = .1;  // Encima del margen (invertido a negativo)
      } else {
        u = -.1;  // Debajo del margen (invertido a positivo)
      }
      double w_d = (u + w * L) / (R);
      double w_i = (u - w * L) / (R);
Serial.print(w_d);
      Serial.print(" ");
      Serial.print(w_i);
      Serial.print(" ");
      // Límites de las velocidades angulares
      double w_limit = 4.51;  // Límite máximo de velocidad angular (rad/s)

      w_d = saturate(w_d, -w_limit, w_limit);
      w_i = saturate(w_i, -w_limit, w_limit);
Serial.print(w_d);
      Serial.print(" ");
      Serial.print(w_i);
      Serial.print(" ");



      ////////////
      sp1 = w_d * R;
      sp2 = w_i * R;

    
    Serial.print(distanciaX);
      Serial.print(" ");
      Serial.print(w);
      Serial.print(" ");
      Serial.print(u);
      Serial.print(" ");
      Serial.print(sp1);
      Serial.print(" ");
      Serial.println(sp2);
    }
    pv1_ = pv1 * (2 * PI * R / 60);

    pv2_ = pv2 * (2 * PI * R / 60);
    ///////////////////////////////////////////////////////////////////////////////////////////////////////


    if (s1 < 5 || s1 > 2000) {
      s1 = -1;  // Valor fuera de rango
    }

    if (s2 < 5 || s2 > 2000) {
      s2 = -1;  // Valor fuera de rango
    }
    if ((s1 >= 50 && s1 <= 300) || (s2 >= 50 && s2 <= 300)) {
      // Condición 1: S1 entre 5 y 30 mm, S2 > 30 mm
      if (s1 >= 50 && s1 <= 300 && s2 >= 50 && s2 <= 300) {
        u = -0.5;
        w = 0;
      }
      // Condición 2: S1 > 30 mm, S2 entre 5 y 30 mm
      else if (s2 >= 50 && s2 <= 300) {
        w = 0.5;

        u = 0;
      }
      // Condición 3: S1 entre 5 y 30 mm, S2 entre 5 y 30 mm
      else if (s1 >= 50 && s1 <= 300) {
        w = -0.5;
        u = 0;
      }






      double w_d = (u + w * L) / (R);
      double w_i = (u - w * L) / (R);

      // Límites de las velocidades angulares
      double w_limit = 4.51;  // Límite máximo de velocidad angular (rad/s)

      w_d = saturate(w_d, -w_limit, w_limit);
      w_i = saturate(w_i, -w_limit, w_limit);
      sp1 = w_d * R;
      sp2 = w_i * R;
    }


    static unsigned long previousTime3 = 0;
    unsigned long currentTime3 = millis();
    tiempo_muestreo3 = (currentTime3 - previousTime3) / 1000.0;
    previousTime3 = currentTime3;


    cv3 = pid1(sp1, pv1_, tiempo_muestreo3);
    cv3_ = mapCustom(cv3, -.23, .23, -255, 255);
    cv3_ = saturate(cv3_, -255, 255);

    cv4 = pid2(sp2, pv2_, tiempo_muestreo3);
    cv4_ = mapCustom(cv4, -.23, .23, -255, 255);
    cv4_ = saturate(cv4_, -255, 255);
    //  SerialBT.print("             ");
    // SerialBT.print(sp1);
    // SerialBT.print(" ");
    // SerialBT.print(sp2);

    // SerialBT.print(" ");
    // SerialBT.print(int(pv1));
    // SerialBT.print(" ");
    // SerialBT.print(int(pv2));
    // SerialBT.print(" ");
    // SerialBT.print(int(cv3_));
    // SerialBT.print(" ");
    // SerialBT.println(int(cv4_));
    // cv3_ = 255;
    if (sp1 >= -0.01 && sp1 <= 0.01) {
      analogWrite(LPWM1, 0);
      analogWrite(RPWM1, 0);
    } else if (cv3_ >= 0) {
      analogWrite(RPWM1, cv3_);
      analogWrite(LPWM1, 0);




    } else {



      analogWrite(LPWM1, abs(cv3_));  // PWM negativo
      analogWrite(RPWM1, 0);          // PWM positivo desactivado
    }

    if (sp2 >= -0.01 && sp2 <= 0.01) {
      analogWrite(LPWM2, 0);
      analogWrite(RPWM2, 0);
    }

    else if (cv4_ >= 0) {
      analogWrite(RPWM2, cv4_);  // PWM positivo
      analogWrite(LPWM2, 0);     // PWM negativo desactivado
    } else {
      analogWrite(LPWM2, abs(cv4_));  // PWM negativo
      analogWrite(RPWM2, 0);          // PWM positivo desactivadoi
    }
    Serial.println(String(sp1) + "XA" + String(pv1_, 2) + "YA" + String(sp2, 2) + "PA" + String(pv2_, 2));
    // Detener el cronómetro
    unsigned long endTime = millis();

    // Calcular el tiempo total de lectura
    unsigned long elapsedTime = endTime - startTime;
    // Serial.println(elapsedTime);
  }

  // Calc}ular odometría
  odometria();

  // Leer el valor de SP desde Bluetooth


  // Imprimir SP, PV y odometría cada segundo
  if ((currentMillis - printMillis) >= 2000) {
    printMillis = currentMillis;

    lastTime = millis();  // Actualizar el tiempo de referencia
    mensajeCounter++;     // Incrementar el contador de mensajes

    boyluobGeneral = "M" + String(mensajeCounter) + "XA" + String(x, 2) + "YA" + String(y, 2) + "PA" + String(phi, 2) + "*";

    // boyluobGeneral = "M" + String(error5) + "XA" + String(sp5, 2) + "YA" + String(phi, 2) + "PA" + String(mensajeCounter, 2) + "*";





    ///////////////////////////////////////////////////////////////////////////////////////////

    // Serial.println(boyluobGeneral);    // Imprimir en el monitor serie



    SerialBT.println(boyluobGeneral);  // Enviar mensaje adicional por Bluetooth

    //     // Imprimir resultados en una sola línea
    //     Serial.print(F("S1 S2 [mm]: "));

    //     if (s1 != -1) {
    //       Serial.print(s1);
    //     } else {
    //       Serial.print(F("   "));  // Espacio vacío si está fuera de rango
    //     }

    //     Serial.print(F(" "));  // Espacio entre S1 y S2

    //     if (s2 != -1) {
    //       Serial.print(s2);
    //     } else {
    //       Serial.print(F("   "));  // Espacio vacío si está fuera de rango
    //     }


    //     Serial.println();  // Nueva línea


    //     Serial.print(u);
    //     Serial.println(w);


    // Serial.print()
  }


  while (SerialBT.available() > 0) {  // Si hay datos disponibles por Bluetooth
    char c = SerialBT.read();         // Leer un carácter del puerto serie Bluetooth

    if (c == '*') {                // Si el carácter es '*', procesar el comando
      if (comando.length() > 0) {  // Asegurarse de que el comando no esté vacío
        procesarMensaje(comando);  // Procesar el comando completo
      }
      comando = "";  // Limpiar el comando una vez procesado
    } else {
      comando += c;  // Agregar el carácter al comando
    }
  }
}
void odometria() {

  deltaRd = (-2 * PI * (contador1 - cd1) * R / (IMP * Z_w * tiempo_muestreo)) * 1.62;
  cd1 = contador1;  // Actualizar el contador anterior
  contador1 = 0;    // Reiniciar contador para evitar acumulación

  deltaRi = (-2 * PI * (contador2 - ci1) * R / (IMP * Z_w * tiempo_muestreo)) * 1.62;
  ci1 = contador2;  // Actualizar el contador anterior
  contador2 = 0;    // Reiniciar contador para evitar acumulación

  x = x + cos(phi) * (deltaRd + deltaRi) / 2;
  y = y + sin(phi) * (deltaRd + deltaRi) / 2;
  phi = phi + ((deltaRd - deltaRi) / L) * .92;

  // Asegurarse de que phi esté entre 0 y 2π
  phi = fmod(phi, 2 * M_PI);  // Resto módulo 2π
  if (phi < 0) {
    phi += 2 * M_PI;  // Ajustar para que sea positivo
  }
}





// Interrupción del Motor 1
void interrupcion1() {
  if (digitalRead(pinB) == HIGH) {
    contador1++;
    contador1b++;  // Incrementar la variable asociada
  } else {
    contador1--;
    contador1b--;  // Decrementar la variable asociada
  }
}

// Interrupción del Motor 2
void interrupcion2() {
  if (digitalRead(pinB2) == HIGH) {
    contador2++;
    contador2b++;  // Incrementar la variable asociada

  } else {
    contador2--;
    contador2b--;  // Decrementar la variable asociada
  }
}
