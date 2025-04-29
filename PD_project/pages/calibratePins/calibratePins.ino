

//sensor
const int echo = 5;
const int trig = 6;  

//relay pins
const int r1 = 7;
const int r2 = 8; 

// conveyor pin assignments
const int motor_step = 11;
const int motor_dir = 12;
const int motor_ena = 13;


//read pin assignments
const int startPin = A0;
const int enaPin = A1;
const int v1Pin = A2;
const int v2Pin = A3;
const int v3Pin = A4;


//setup var
int start, ena, v1, v2, v3, var, step, caneIn;
int position = 1;



void setup() {
  Serial.begin(9600);
  pinMode(5, OUTPUT);
  pinMode(6, INPUT);

//relay
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  digitalWrite(r1,HIGH);
  digitalWrite(r2,HIGH);
  
//motors
  pinMode(motor_ena, OUTPUT);
  pinMode(motor_step, OUTPUT);
  pinMode(motor_dir, OUTPUT);
  digitalWrite(motor_ena, LOW);

  pinMode(startPin, INPUT);
  pinMode(enaPin, INPUT);
  pinMode(v1Pin, INPUT);
  pinMode(v2Pin, INPUT);
  pinMode(v3Pin, INPUT);
  
  digitalWrite(6, LOW);
  
  Serial.println("Setup Complete");

}

void loop() {

  
  Serial.println("-----------------");
  caneIn = digitalRead(6);
  Serial.print("echo:  ");
  Serial.println(caneIn);

  start = digitalRead(startPin);
  Serial.print("start: ");
  Serial.println(start);
  
  
  ena = digitalRead(enaPin);
  Serial.print("ena:   ");
  Serial.println(ena);

  
  v1 = digitalRead(v1Pin);
  Serial.print("v1: ");
  Serial.println(v1);

  
  v2 = digitalRead(v2Pin);
  Serial.print("v2: ");
  Serial.println(v2);

  
  v3 = digitalRead(v3Pin);
  Serial.print("v3: ");
  Serial.println(v3);
  
  Serial.println("-----------------");
  
  delay(1000);
  
}
