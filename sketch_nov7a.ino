#include <Servo.h>

const byte NOMBRE = 4;
const byte BROCHES[NOMBRE] = {3, 5, 7, 9};
const int NEUTRES[NOMBRE] = {1500, 1500, 1500, 1500};
const int VITESSE = 50; // Ecart au neutre en microsecondes, pas des tr/min.

Servo servos[NOMBRE];
char message[4];
byte longueur = 0;
bool invalide = false;
unsigned long dernierMessage = 0;

void arreter() {
  for (byte i = 0; i < NOMBRE; i++)
    servos[i].writeMicroseconds(NEUTRES[i]);
}

void setup() {
  Serial.begin(9600);
  for (byte i = 0; i < NOMBRE; i++) {
    servos[i].writeMicroseconds(NEUTRES[i]);
    servos[i].attach(BROCHES[i]);
  }
  arreter();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      if (longueur == 4 && !invalide) {
        for (byte i = 0; i < NOMBRE; i++) {
          int direction = message[i] - '1'; // 0=-1, 1=arret, 2=+1
          servos[i].writeMicroseconds(NEUTRES[i] + direction * constrain(VITESSE, 0, 250));
        }
        dernierMessage = millis();
        Serial.print("OK:");
        for (byte i = 0; i < NOMBRE; i++) Serial.print(message[i]);
        Serial.println();
      }
      longueur = 0;
      invalide = false;
    } else if (longueur < 4 && c >= '0' && c <= '2') {
      message[longueur++] = c;
    } else {
      invalide = true;
    }
  }
  if (millis() - dernierMessage > 300) arreter();
}
