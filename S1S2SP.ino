#include <Wire.h>              // Incluye librería bus I2C
#include <MechaQMC5883.h>      // Incluye librería para magnetómetro QMC5883L

MechaQMC5883 qmc;              // Crea objeto

const int drdyPin = 23;         // Define el pin conectado a DRDY
const int powerPin = 27;        // Define el pin que controla la alimentación del sensor

#include <Wire.h>
#include <Adafruit_VL53L0X.h>

// Declaramos dos objetos para los sensores VL53L0X
Adafruit_VL53L0X sensor1 = Adafruit_VL53L0X();
Adafruit_VL53L0X sensor2 = Adafruit_VL53L0X();


// Pines para XSHUT (shutdown) de cada sensor
#define XSHUT1 4 // Pin para XSHUT del sensor 1
#define XSHUT2 5 // Pin para XSHUT del sensor 2


unsigned long previousMillisLED = 0;




bool ledState = LOW;
void setup() {
  pinMode(drdyPin, INPUT);     // Configura el pin DRDY como entrada
  pinMode(powerPin, OUTPUT);   // Configura el pin de alimentación como salida

  digitalWrite(powerPin, HIGH); // Apaga la alimentación del sensor
  Serial.begin(115200);        // Inicializa monitor serie
  Serial.println("Sensor apagado. Esperando 5 segundos...");
    // delay(5000); 
  
    pinMode(XSHUT1, OUTPUT);
  pinMode(XSHUT2, OUTPUT);


  // Configuración de I2C (Wire)
  Wire.begin();

  Serial.println("Iniciando sensores...");

  // Apagamos ambos sensores antes de inicializarlos
  digitalWrite(XSHUT1, LOW);  // Apagamos el sensor 1
  digitalWrite(XSHUT2, LOW);  // Apagamos el sensor 2
  delay(50);

  // Inicializamos el primer sensor
  digitalWrite(XSHUT1, HIGH); // Encendemos el sensor 1
  delay(100); // Retraso más largo

  if (!sensor1.begin()) {
    Serial.println(F("Error al iniciar el sensor 1. Verifica conexiones y alimentación."));
    while (1); // Detenemos el programa si no se inicializa
  }
  sensor1.setAddress(0x30); // Cambiamos la dirección del sensor 1 a 0x30

  // Inicializamos el segundo sensor
  digitalWrite(XSHUT2, HIGH); // Encendemos el sensor 2
  delay(100); // Retraso más largo

  if (!sensor2.begin()) {
    Serial.println(F("Error al iniciar el sensor 2. Verifica conexiones y alimentación."));
    while (1); // Detenemos el programa si no se inicializa
  }
  sensor2.setAddress(0x31); // Cambiamos la dirección del sensor 2 a 0x31
  
  Serial.println(F("Sensores listos"));
  
  ///////////////                // Espera 5 segundos

  digitalWrite(powerPin, LOW); // Enciende la alimentación del sensor
  Serial.println("Sensor encendido. Esperando datos...");
delay(100);
  qmc.init();                  // Inicializa objeto QMC5883L

  // Espera hasta que DRDY esté en HIGH
  // while (digitalRead(drdyPin) == LOW) {
  //   Serial.println("Esperando datos...");
  //   qmc.init();

  //   delay(100);  // Revisa el estado de DRDY cada 100 ms
  // }
  Serial.println("Datos disponibles. Iniciando el loop...");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillisLED >= 100) {
    previousMillisLED = currentMillis;  // Actualiza el tiempo previo del LED
    ledState = !ledState;               // Alterna el estado del LED
    digitalWrite(27, ledState);
  }
  int x, y, z;                 // Variables de los 3 ejes
  float acimut, geografico;    // Variables para acimut magnético y geográfico
  float declinacion = 2.55;    // Declinación desde página: http://www.magnetic-declination.com/

  qmc.read(&x, &y, &z, &acimut);  // Lectura de los ejes y acimut magnético
  geografico = 360 - (acimut + declinacion);  // Invertimos el azimut geográfico

  // Ajustar para que siempre esté en el rango 0 a 360
  if (geografico < 0) {                // Si el valor es negativo,
    geografico += 360;                 // ajustamos sumando 360.
  }

  if (geografico >= 360) {             // Si el valor excede 360,
    geografico -= 360;                 // ajustamos restando 360.
  }
  // Serial.print("Acimut geográfico: ");
  // Serial.print(geografico, 0);       // Muestra valor de acimut geográfico sin decimales
  // Serial.print(" grados |");


delay(200);

  
VL53L0X_RangingMeasurementData_t measure1, measure2;






  // Leer el sensor 1
  sensor1.rangingTest(&measure1, false);  // No debug output
  int distance1 = measure1.RangeMilliMeter;

  // Leer el sensor 2
  sensor2.rangingTest(&measure2, false);  // No debug output
  int distance2 = measure2.RangeMilliMeter;

  // Aplicar saturación: solo mostrar valores entre 5 mm y 2000 mm
  if (distance1 < 5 || distance1 > 2000) {
    distance1 = -1;  // Valor fuera de rango
  }
  
  if (distance2 < 5 || distance2 > 2000) {
    distance2 = -1;  // Valor fuera de rango
  }
Serial.print("SP");


Serial.print(geografico * ( 3.1415 / 180));
  // Formato SA + s1 + SB + s2 + *
  Serial.print("SA");

  // Si la distancia 1 es válida, la enviamos, de lo contrario -1
  Serial.print(distance1);

  Serial.print("SB");

  // Si la distancia 2 es válida, la enviamos, de lo contrario -1
  Serial.print(distance2);

  Serial.println("*");  // Fin del formato

  delay(200 );  // Demora de 100 ms
  
  

}





