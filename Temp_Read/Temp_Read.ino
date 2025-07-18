#include <OneWire.h>

// 温度センサーのデータピンをD12に設定
const int DS18S20_Pin = 12;
OneWire ds(DS18S20_Pin);

// 温度取得関数（前回と同じものです）
float getTemp() {
  byte data[12];
  byte addr[8];
  if (!ds.search(addr)) {
    ds.reset_search();
    return -1000.0;
  }
  if (OneWire::crc8(addr, 7) != addr[7]) {
    return -1000.0;
  }
  if (addr[0] != 0x10 && addr[0] != 0x28) {
    return -1000.0;
  }
  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1);
  delay(750);
  ds.reset();
  ds.select(addr);
  ds.write(0xBE);
  for (int i = 0; i < 9; i++) {
    data[i] = ds.read();
  }
  byte MSB = data[1];
  byte LSB = data[0];
  float tempRead = ((MSB << 8) | LSB);
  float temperature = tempRead / 16.0;
  return temperature;
}

void setup() {
  // シリアル通信を開始 (ボーレート: 115200)
  Serial.begin(115200);
}

void loop() {
  float temp = getTemp();
  
  // 温度が正しく読み取れた場合のみ、数値を送信
  if (temp != -1000.0) {
    // パソコン側で処理しやすいように、数値だけを送ります
    Serial.println(temp);
  }
  
  // 5秒ごとに測定（記録間隔はここで調整）
  delay(5000); 
}