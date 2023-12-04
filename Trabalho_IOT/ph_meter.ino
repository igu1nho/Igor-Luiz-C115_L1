#include <ESP8266WiFi.h>

// Configurações do Wi-Fi e ThingSpeak
const char* ssid = "WLL-Inatel"; // Substitua com o nome da sua rede Wi-Fi
const char* password = "inatelsemfio"; // Substitua com a senha da sua rede Wi-Fi
const char* server = "api.thingspeak.com"; // Servidor do ThingSpeak
String apiKey = "4XRQUUDKQZUNSEXX"; // Sua chave de API do ThingSpeak

const int potPin = A0; // Pino do potenciômetro

WiFiClient client;

void setup() {
  Serial.begin(9600);
  pinMode(potPin, INPUT);

  // Conexão Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(2000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  int sensorValue = analogRead(A0);
  float ph = sensorValue * (14.0/1023.0);

  Serial.print("PH: ");
  Serial.println(ph);

  // Envia para o ThingSpeak
  if (client.connect(server, 80)) {
    String postStr = apiKey;
    postStr += "&field1=";
    postStr += String(ph);
    postStr += "\r\n";

    client.print("POST /update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(postStr.length());
    client.print("\n\n");
    client.print(postStr);
  }

  delay(1000); // Aguarda antes de enviar o próximo valor
}
