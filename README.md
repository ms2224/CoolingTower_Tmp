# CoolingTower_Tmp
冷却塔温度記録用

冷却塔の冷却性能を循環する水の温度変化を記録することで評価する

1. 温度計測装置 
    - 水槽に作った温度計を流用 [SwitchScience_DS18B20](https://ssci.to/4908)
    - Arduino Uno

2. 温度計計測プログラム
    - [Temp_Read.ino](https://github.com/ms2224/CoolingTower_Tmp/blob/main/Temp_Read/Temp_Read.ino) : OneWireで温度を取得しSerialPrint

3. 温度記録＆モニタープログラム
    - [log_temp_graph.py](https://github.com/ms2224/CoolingTower_Tmp/blob/main/log_temp_graph.py) : datファイルに時間と温度を記録しグラフをリアルタイムで表示する