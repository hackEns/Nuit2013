#define SERIAL_SPEED 115200

byte incoming_byte;
int compteur = -1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(SERIAL_SPEED);
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
        Serial.print(incoming_byte);
      }
    }
    // Paquet de couleur
    else {
      // Si compteur <= 12, forward sur Serial1
      if(compteur <= 12) {
        Serial.print(incoming_byte);
      }
    }
  }
}
