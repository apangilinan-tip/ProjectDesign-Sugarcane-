
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
int start, ena, v1, v2, v3, step, caneIn;
int position = 1;
int var = 1;


void setup() {
  Serial.begin(9600);
  
//sensor
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

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

  Serial.println("Setup Complete");
}

void loop() {
  var = readVar();
  Serial.println("-----------------------");
  Serial.print("Variety: ");
  Serial.println(var);
  if (var!=0 && var!=6 && var!=7){
    step = det_position(var);
    
    Serial.print("sorter rotating. Steps = ");
    Serial.println(step);
    sorter(step);
    position = var;}

}

void sorter(int step){
  int vel = 500;
  int cal = 800;
  if (step<0){
    digitalWrite(motor_dir, LOW);
    step=abs(step);
    for (int i=0; i<step; i++){
      for (int x = 0; x< cal; x++){
        digitalWrite(motor_step,HIGH);
        delayMicroseconds(vel);
        digitalWrite(motor_step,LOW);
        delayMicroseconds(vel);}
    }
  }

  else if(step>0){
    digitalWrite(motor_dir, HIGH);    
    step=abs(step);
    for (int i=0; i<step; i++){
      for (int x = 0; x< cal; x++){
        digitalWrite(motor_step,HIGH);
        delayMicroseconds(vel);
        digitalWrite(motor_step,LOW);
        delayMicroseconds(vel);}
    }
  }  
}

int det_position(int var){
  int step;
  int toGo = position - var;

  if (toGo == -4){step = 1;}
  else if(toGo == -3){step = 2;}
  else if(toGo == 4){step = -1;}
  else if(toGo == 3){step = -2;}
  else {step = toGo;}
    
  return step;
}

int readVar(){
  int variety = 0;
  float v1 = digitalRead(v1Pin);
  float v2 = digitalRead(v2Pin);
  float v3 = digitalRead(v3Pin);
  
  if (v1==1) variety += 1;
  if (v2==1) variety += 2;
  if (v3==1) variety += 4;
  
  return variety;
}
