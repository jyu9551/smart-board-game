// DC Motor
const int ENA = 9;  // Enable pin
const int IN1 = 8;  
const int IN2 = 7;
// LED
int LED_1 = 3;  // Yellow LED
int LED_2 = 4;  // Green LED
int LED_3 = 5;  // Blue LED
int LED_4 = 6;  // Red LED

void setup() {

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(LED_1,OUTPUT);
  pinMode(LED_2,OUTPUT);
  pinMode(LED_3,OUTPUT);
  pinMode(LED_4,OUTPUT);

  Serial.begin(9600);   // Baud Rate
}

void loop() {

  if (Serial.available() > 0) { 
    char command = Serial.read();  // Read 'command' from Python Game

    // Game Start
    if (command == 's'){ 
      for(int i = 0; i<7; i++){
        digitalWrite(LED_1, HIGH); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(50);
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, HIGH); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(50);
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, HIGH); digitalWrite(LED_4, LOW);
        delay(50);
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, HIGH);
        delay(50);
      }
      for(int i = 0; i<7; i++){
        digitalWrite(LED_1, HIGH); digitalWrite(LED_2, LOW); digitalWrite(LED_3, HIGH); digitalWrite(LED_4, LOW);
        delay(100);
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, HIGH); digitalWrite(LED_3, LOW); digitalWrite(LED_4, HIGH);
        delay(100);
      }
      for(int i = 0; i<7; i++){
        digitalWrite(LED_1, HIGH); digitalWrite(LED_2, HIGH); digitalWrite(LED_3, HIGH); digitalWrite(LED_4, HIGH);
        delay(100);
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(100);
      }
    }

    // LED color means Player number
    if (command == '0') {  // Player 0, Toggle Yellow LED
      for(int i = 0; i<7; i++) {
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(200); // 200ms delay
        digitalWrite(LED_1, HIGH); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(200);
      }
    } else if (command == '1') {  // Player 1, Toggle Green LED
      for(int i = 0; i<7; i++) {
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(200);
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, HIGH); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(200);
      }
    } else if (command == '2') {  // Player 2, Toggle Blue LED
      for(int i = 0; i<7; i++){
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(200);
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, HIGH); digitalWrite(LED_4, LOW);
        delay(200);
      }
    } else if (command == '3') {  // Player 3, Toggle Red LED
      for(int i = 0; i<7; i++){
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, LOW);
        delay(200);
        digitalWrite(LED_1, LOW); digitalWrite(LED_2, LOW); digitalWrite(LED_3, LOW); digitalWrite(LED_4, HIGH);
        delay(200);
      }
    }

    // Motor Control
    if (command == 'r'){
      // (Door Open)
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      analogWrite(ENA, 255);  // PWM 신호를 이용하여 모터 속도 조절 (255 is Max Speed)
      delay(8000);  // 8 second

      // (Door Close)
      digitalWrite(IN1,HIGH);
      digitalWrite(IN2,LOW);
      delay(8450); 

      // Stop Motor
      digitalWrite(IN1,LOW);
      digitalWrite(IN2,LOW);
      delay(200);
    }

    delay(100);
  }
}
