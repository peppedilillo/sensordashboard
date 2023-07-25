/*
This program provides a serial interface with the HM1520LF relative humidity sensor
https://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Data+Sheet%7FHPC091_C%7FA1%7Fpdf%7FEnglish%7FENG_DS_HPC091_C_A1.pdf%7FCAT-HSA0003

The program converts the analog read on pin A0, connected with the sensor analog output, and provide the time and value of the readout (csv)
after a read command is sent on the serial port. 
  !R -> Read the raw value (Voltage output in mV)
  !C -> Read the converted value (RH %)

Credits: Yuri Evangelista
*/
char inByte[3];
unsigned long startTime;

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
Serial.setTimeout(1000);
while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

}

void loop() {
  if (Serial.available() > 0) {
    int sensorValue = analogRead(A0);
    float voltage = sensorValue * (5.0 / 1023.0) * 1000;
    float RH = 0.195 * voltage/5 - 38.5;
    //Serial.println(Serial.available());
    //Serial.readBytes(inByte,20);
    int charsRead = Serial.readBytesUntil('\n', inByte, sizeof(inByte) - 1);  // Look for newline or max of 19 chars
    if (inByte[0] == 33 && inByte[1] == 82) { //prints the raw value (in mV) only if receives a "!R"
      Serial.print(millis());
      Serial.print(", ");
      Serial.println(voltage);
      inByte[0] = '\0';
      inByte[1] = '\0';
    } 
    if (inByte[0] == 33 && inByte[1] == 67) { //prints the converted value (in Rh%) only if receives a "!C"
      Serial.print(millis());
      Serial.print(", ");
      Serial.println(RH);
      inByte[0] = '\0';
      inByte[1] = '\0';
    }
  }
}


