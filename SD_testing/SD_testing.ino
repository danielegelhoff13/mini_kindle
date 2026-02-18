#include <SPI.h>
#include <SD.h>

#define SD_CS 17
#define DISP_CS 5

void setup() {
  Serial.begin(115200);
  delay(3000);

  // Make sure display CS is HIGH before SD starts
  pinMode(DISP_CS, OUTPUT);
  digitalWrite(DISP_CS, HIGH);

  if (!SD.begin(SD_CS)) {
    Serial.println("SD init failed!");
    while (1);
  }

  Serial.println("SD initialized.");

  uint8_t buf[100];

  File file = SD.open("test.txt", FILE_READ);
  if (file) {
    Serial.println("Reading file:");

    while (file.available()) {
      Serial.write(file.read());  // write prints raw char
    }

    file.close();
    Serial.println("\nDone.");
  } else {
    Serial.println("Error opening file");
  }


}

void loop() {

  Serial.println("standby");
  delay(5000);
}
