
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
  
  start = digitalRead(startPin);
  while (start == 1){

      ena = digitalRead(enaPin);

      if (ena==1){
          Serial.print("Input detected. Ena: ");
          Serial.println(ena);
  
          var = readVar();
          Serial.print("Variety: ");
          Serial.println(var);
  
          if (var!=0 && var!=6 && var!=7){
              step = det_position(var);
              Serial.print("sorter rotating. Steps = ");
              Serial.println(step);
              sorter(step);
              
              digitalWrite(trig, HIGH);
              while(true){
                Serial.println("Sorter Status: waiting for cane");
                caneIn = digitalRead(echo);
                if (caneIn == HIGH){
                  Serial.println("Cane Status: CANE IN THE SORTER!");
                  break; }
              }
              digitalWrite(trig, LOW); 
          }
  
          if (var == 0){}
          if (var == 6){}
          if (var == 7){}
      }
      Serial.println("Sorter Status: waiting for INPUT");
      start = digitalRead(startPin);
  }
  Serial.println("Waiting for start:");
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

  
void emptyContainer(){

  digitalWrite(r1,HIGH);
  digitalWrite(r2,LOW);
  delay(5000);
  digitalWrite(r1,LOW);
  digitalWrite(r2,HIGH);
  delay(5000);
  digitalWrite(r1,LOW);
  digitalWrite(r2,LOW);

}

int det_position( int value){
    int step;
    int toGo = position - value;
    
    if (toGo = 1 || toGo == -4) {step=1;}
    else if (toGo = 2 || toGo == -3) {step=2;}
    else if (toGo = -1 || toGo == 4) {step=-1;}
    else if (toGo = -2 || toGo == 3) {step=-2;}
    return step;

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

  else{
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
