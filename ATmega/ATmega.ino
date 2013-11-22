/*
Pins :
======
15 : Led R
16 : Led G
17 : Led B

Paquets serial :
================
[synchro = 1]
[fonction] => 2 bits
[compteur] => 5 bits
    ===
[synchro = 0]
[couleurR] => 7 bits
    ===
[synchro = 0]
[couleurG] => 7 bits
    ===
[synchro = 0]
[couleur B] => 7 bits

Fonctions :
===========
0 => Switch immédiat
1 => Fade in
2 => Broadcast => applique le paquet et le forward quand même
3 => Automatique
*/

#define R 0
#define G 1
#define B 2
const int pins[3] = {15, 16, 17};

#define SERIAL_SPEED 19200
#define DEBUG 0

int duty[3] = {0, 0, 0};

int serial_i = -1;
byte incoming_byte;

void setup() {
  Serial.begin(SERIAL_SPEED);
}

void loop() {
  // Note : no need for pinMode before analogWrite
  analogWrite(pins[R], duty[R]);
  analogWrite(pins[G], duty[G]);
  analogWrite(pins[B], duty[B]);
  
  if(DEBUG) {
    Serial.print("R : ");
    Serial.println(duty[R]);
    Serial.print("G : ");
    Serial.println(duty[G]);
    Serial.print("B : ");
    Serial.println(duty[B]);
  }
}

void serialEvent() {
  //serialEvent est appelée à la fin de la boucle si des données sont dispos sur le RX
  while(Serial.available()) {
    incoming_byte = (byte) Serial.read();
    
    if(highByte(incoming_byte)) {
      // Header
      int serial_i = incoming_byte & B00011111; // serial_i = compteur
      // Note: serial_i = 0 => à traiter
      
      // Note : [Unused] serial_fonction = (incoming_byte >> 5) & B011;
      
      if(serial_i != 0) {
        // Forward
        Serial.print((incoming_byte & B11100000) | (serial_i - 1)); // Décrément du compteur
      }
      
      if(incoming_byte && B01100000 == 2) {
        // Broadcast
        Serial.print(incoming_byte & B11100000); // Forward avec compteur nul
      }
    }
    else {
      // Paquet de couleur
      if(serial_i != -1) {
        // Si on doit traiter le paquet, on le fait
        duty[serial_i] = (incoming_byte & B01111111) << 1;
        serial_i++;
      }
      else {
        // Sinon, on forward tel quel
        Serial.print(incoming_byte);
      }
    }
    serial_i = -1;
  }
}
