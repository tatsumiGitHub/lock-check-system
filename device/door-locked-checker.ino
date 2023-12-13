#define THRESHOLD 10

void setup() {
  // put your setup code here, to run once:
  pinMode(11, OUTPUT);
  pinMode(8, OUTPUT);
  digitalWrite(2, HIGH);
  digitalWrite(3, HIGH);

  pinMode(7, OUTPUT);
  pinMode(12, OUTPUT);
  digitalWrite(7, HIGH);
  digitalWrite(12, HIGH);

  pinMode(9, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(9, HIGH);
  digitalWrite(13, HIGH);

  pinMode(6, OUTPUT);
  pinMode(10, OUTPUT);
  digitalWrite(6, HIGH);
  digitalWrite(10, HIGH);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  long x, y, z;
  x = analogRead(3) - 510;
  y = analogRead(4) - 510;
  z = analogRead(5) - 540;
  Serial.println("1001001," + String(x) + "," + String(y) + "," + String(z));
  if (50 < z) {
    digitalWrite(13, LOW);
  } else if (z < -50) {
    digitalWrite(6, LOW);
  } else {
    digitalWrite(13, HIGH);
    digitalWrite(6, HIGH);
  }
  if (50 < x) {
    digitalWrite(10, LOW);
  } else if (x < -50) {
    digitalWrite(9, LOW);
  } else {
    digitalWrite(9, HIGH);
    digitalWrite(10, HIGH);
  }
  if (50 < y) {
    if (-30 < x) {
      digitalWrite(7, LOW);
    }
    if (x < 30) {
      digitalWrite(8, LOW);
    }
  } else if (y < -50) {
    if (-30 < x) {
      digitalWrite(11, LOW);
    }
    if (x < 30) {
      digitalWrite(12, LOW);
    }
  } else {
    digitalWrite(8, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(12, HIGH);
    digitalWrite(11, HIGH);
  }
  delay(100);
}