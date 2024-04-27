void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  pinMode(8, LOW);
}

void loop() {
  if(Serial.available() > 0){
    pinMode(8, HIGH);
    delay(10);
  } else {
    pinMode(8, LOW);
  }
}
