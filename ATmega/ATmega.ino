#define R 0
#define G 1
#define B 2
const int pins[3] = {15, 16, 17};

#define SERIAL_SPEED 115200

int serial_i = -1;
byte incoming_byte;

void setup() {
    Serial.begin(SERIAL_SPEED);
}

void loop() {
    if(Serial.available()) {
        incoming_byte = (byte) Serial.read();

        // Header
        if(highByte(incoming_byte)) {
            serial_i = incoming_byte & B00111111;

            // Forward avec décrément du compteur
            if(serial_i != 0) {
                Serial.print((incoming_byte & B11000000) | (serial_i - 1));
                serial_i = -1
            }

            // Broadcast
            if(incoming_byte & B01000000 == B01000000) {
                Serial.print(incoming_byte & B11000000);
            }
        }
        // Paquet de couleur
        else {
            if(serial_i != -1) {
                analogWrite(pins[serial_i], incoming_byte << 1);
                serial_i++;
            }
            else {
                Serial.print(incoming_byte);
            }
        }
    }
}
