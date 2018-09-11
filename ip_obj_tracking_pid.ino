/*
    This sketch sends a message to a TCP server

*/

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

ESP8266WiFiMulti WiFiMulti;

void setup() {
  Serial.begin(115200);
  delay(10);

  // We start by connecting to a WiFi network
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("ROBOTICS SOCIETY", "vssutrobotix");

  Serial.println();
  Serial.println();
  Serial.print("Wait for WiFi... ");

  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(500);
analogWrite(D0, 512);
analogWrite(D1, 512);
analogWrite(D2, 512);
analogWrite(D3, 512);
}

int mx_spd = 200;

void motion(int spd, float area)
{
  
  if(spd<=-50)
  {
    analogWrite(D0,mx_spd-(spd/2));
    analogWrite(D1,0);
    analogWrite(D3,mx_spd-(spd/2));
    analogWrite(D2,0);
  }
  else if(spd>=50)
  {
    analogWrite(D1,mx_spd+(spd/2));
    analogWrite(D0,0);
    analogWrite(D2,mx_spd+(spd/2));
    analogWrite(D3,0); 
  }
  else if((spd<50||spd>-50)&&area==2)
  {
    analogWrite(D0,0);
    analogWrite(D1,0);
    analogWrite(D2,0);
    analogWrite(D3,0);
  }
  else if((spd<50||spd>-50)&&area==1)
  {
    analogWrite(D1,mx_spd+100);
    analogWrite(D0,0);
    analogWrite(D3,mx_spd+100);
    analogWrite(D4,0); 
  }
  else if((spd<50||spd>-50)&&area==0)
  {
    analogWrite(D0,mx_spd+100);
    analogWrite(D1,0);
    analogWrite(D2,mx_spd+100);
    analogWrite(D3,0); 
  }
}


void loop()
{
  const uint16_t port = 1234;
  const char * host = "192.168.1.101"; // ip or dns

  Serial.print("connecting to ");
  Serial.println(host);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;

  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    Serial.println("wait 5 sec...");
    //delay(5000);
    return;
  }
  int spd=0;
  int v;
  int a;
l1:
  spd=0;
  String k = client.readStringUntil('\r');
  //Serial.println(k);
  v=k.toInt();
  spd=v/10;
  if(v<0) v=-1*v;
  a=v%10;
  //Serial.println(spd);
  //Serial.println(a);
  motion(spd,a);
  goto l1;
}
