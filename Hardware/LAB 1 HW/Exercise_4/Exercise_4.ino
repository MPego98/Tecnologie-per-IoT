int motorPin = 9;

int speedy =0;
void setup() {
  pinMode(motorPin, OUTPUT);
  Serial.begin(9600);
   while(!Serial);
  Serial.println("Lab 1.4 Starting");
  

}

void loop() {
  
   if (Serial.available()) {
      char val = Serial.read();
      
      if (val == '+' ) {
        speedy = speedy +5;
        
         
         if(speedy >= 255){
          speedy = 255;
            Serial.println("Already at max speed ");
          }else{
            analogWrite(motorPin, speedy);
            Serial.print("Increasing Speed: ");
            Serial.println(speedy);
          }


         
      }else if (val == '-' ){
         speedy = speedy -5;
         
          if(speedy <= 0){
            speedy = 0;
            Serial.println("Already at min speed ");
          }else{
            analogWrite(motorPin, speedy);
            Serial.print("Decreasing Speed: ");
            Serial.println(speedy);
          }

         
      }


    
      
   }

}
