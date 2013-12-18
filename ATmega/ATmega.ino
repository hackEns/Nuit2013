#define R 0
#define G 1
#define B 2
const int pins[3] = {9, 10, 11};

#define SERIAL_SPEED 115200

int serial_i = -1;
byte incoming_byte;

void setup() {
    Serial.begin(SERIAL_SPEED);

    // Led R to show that microcontroller is ready
    analogWrite(pins[R], 255);
    analogWrite(pins[G], 0);
    analogWrite(pins[B], 0);
}

void loop() {
    if(Serial.available()) {
        incoming_byte = (byte) Serial.read();

        // Header
        if(incoming_byte & B10000000) {
            serial_i = incoming_byte & B00111111;

            // Forward avec décrément du compteur
            if(serial_i != 0) {
                Serial.write(incoming_byte - 1);
                serial_i = -1;
            }

            // Broadcast
            if((incoming_byte & B01000000) == B01000000) {
                Serial.write(B11000000);
            }
        }
        // Paquet de couleur
        else {
            if(serial_i != -1) {
                analogWrite(pins[serial_i], incoming_byte << 1);
                serial_i++;
            }
            else {
                Serial.write(incoming_byte);
            }
        }
    }
}
