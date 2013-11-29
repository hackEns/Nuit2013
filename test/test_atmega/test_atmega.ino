#define R 0
#define G 1
#define B 2
const int pins[3] = {9, 10, 11};

void setup() {
    // Led R to show that microcontroller is ready
    analogWrite(pins[R], 255);
    analogWrite(pins[G], 255);
    analogWrite(pins[B], 255);
}

void loop() {
}
