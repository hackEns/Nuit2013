#define SERIAL_SPEED 115200

byte incoming_byte;
int compteur = -1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(SERIAL_SPEED);
  Serial1.begin(SERIAL_SPEED);
  Serial2.begin(SERIAL_SPEED);
}

void loop() {
  // put your main code here, to run repeatedly: 
  if(Serial.available()) {
    incoming_byte = (byte) Serial.read();
    
    // Header
    if(incoming_byte & B10000000) {
      compteur = incoming_byte & B00111111;
      
      // Si compteur <= 12, forward sur Serial1 (0..12)
      if(compteur <= 12) {
        Serial1.print(incoming_byte);
      }
      // Si compteur > 13, forward sur Serial2 (13..25)
      else {
        Serial2.print((incoming_byte & B11000000) | (compteur - 13));
      }
      
      // Si broadcast, forward sur Serial1 et Serial2
      if(incoming_byte & B01000000 == B01000000) {
          Serial1.print(incoming_byte & B11000000);
          Serial2.print((incoming_byte & B11000000) | (compteur - 13));
      }
    }
    // Paquet de couleur
    else {
      // Si compteur <= 13, forward sur Serial1
      if(compteur <= 12) {
        Serial1.print(incoming_byte);
      }
      // Si compteur > 13, forward sur Serial2
      else {
        Serial2.print((incoming_byte & B11000000) | (compteur - 13));
      }
    }
  }
}
