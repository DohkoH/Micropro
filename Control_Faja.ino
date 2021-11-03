int motor = 7;

void setup() {
  Serial.begin(9600);
  pinMode(motor,OUTPUT);
}

String py;
int Motor = 0;

void loop() {
  if(Serial.available()){
     py = Serial.readString();
     Motor = py.toInt();
     if(py  == " 0 "){ 
      digitalWrite(motor,LOW);
     }
     if (py == "1"){
      digitalWrite(motor,HIGH);
      }
   }
}
