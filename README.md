# tiny-gate
With **tiny-gate** you can collect data from your device using Modbus TCP/IP protocol and store these data into your database or forward them.

You can use this template and adapt it with your system to get quick access on your device.

## Installation
```
sudo apt install python3-pip
pip3 install pymodbus
pip3 install numpy
pip install pysqlite3
```

## Example
```
python3 tiny-gate
```
```
1-configuration
2-load setting

? 1


********** TINY-GATE **********


**PLC**


IPv4 address: 192.168.100.3
Modbus port:  502


**DATABASE**


1:local
2:remote

? 1
database name: tiny-store.db
PLC connection: ONLINE
Successfully Connected to SQLite
------------------------------------
Timestamp:  2022-01-24 08:40:48.349342
Connection state: ONLINE
value 0: 17347.0
value 1: -14417.0
value 2: -64.0
value 3: 0.0
value 4: -64.0
value 5: 0.0
value 6: -64.0
value 7: 0.0
value 8: -64.0
value 9: 0.0
timestamp: 2022-01-24 08:40:48.349342
connection_state: 1
error_code: 0
Execution time: 0.09619808197021484 seconds 
Error code:  0  description:   
------------------------------------
```




