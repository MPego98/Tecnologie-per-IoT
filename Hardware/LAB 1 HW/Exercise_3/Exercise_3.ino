int led = 13 ;// define LED Interface

volatile int person = 0;

void setup ()
{
 
  Serial.begin(9600);
  pinMode(led, OUTPUT);

  Serial.println("Lab 1.3 Starting: ");
  attachInterrupt(digitalPinToInterrupt(3), inter_Sound, CHANGE);

}
void loop ()
{
   Serial.print("Person: ");
   Serial.println(person);
   delay(30000);
}


void inter_Sound()
{
    person = person +1;
   digitalWrite(led, !digitalRead(3));
   
     
     delay(5000);

}
