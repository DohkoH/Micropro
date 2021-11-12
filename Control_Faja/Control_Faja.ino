int motor = 7;

void setup() {
  Serial.begin(9600);
  pinMode(motor,OUTPUT);
  digitalWrite(motor,LOW);
}

int py;
int Motor = 0,vMotor= 0;

void loop() {
  if (Serial.available()){
     Motor = Serial.read();
     Serial.print(Motor);
     if (Motor=='0'){
        digitalWrite(motor,LOW);
      }
      else if (Motor=='1'){
        digitalWrite(motor,HIGH);
        }
       else{
        Motor=0;
        }
      }
     }
