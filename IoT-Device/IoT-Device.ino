void setup() {
  // put your setup code here, to run once:
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  long x, y, z;
  x = analogRead(3) - 510;
  y = analogRead(4) - 510;
  z = analogRead(5) - 540;
  Serial.println("device_name," + String(x) + "," + String(y) + "," + String(z));
  if (50 < z) {
    digitalWrite(13, HIGH);
  } else if (z < -50) {
    digitalWrite(6, HIGH);
  } else {
    digitalWrite(6, LOW);
    digitalWrite(13, LOW);
  }
  if (50 < x) {
    digitalWrite(10, HIGH);
  } else if (x < -50) {
    digitalWrite(9, HIGH);
  } else {
    digitalWrite(9, LOW);
    digitalWrite(10, LOW);
  }
  if (50 < y) {
    if (-30 < x) {
      digitalWrite(7, HIGH);
    }
    if (x < 30) {
      digitalWrite(8, HIGH);
    }
  } else if (y < -50) {
    if (-30 < x) {
      digitalWrite(11, HIGH);
    }
    if (x < 30) {
      digitalWrite(12, HIGH);
    }
  } else {
    digitalWrite(7, LOW);
    digitalWrite(8, LOW);
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
  }
  delay(100);
}