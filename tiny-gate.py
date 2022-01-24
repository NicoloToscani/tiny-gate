from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from datetime import datetime
from enum import Enum
import time
import sqlite3
import configparser
import numpy as np

conf_3 ='1:local'
conf_4 ='2:remote'
conf_1 = '1-configuration'
conf_2 = '2-load setting'

# Define connection state
#class ConnectionState(Enum):
    # OFFLINE = 0
    # ONLINE = 1

# Connection state init
connection_state = 0

write = '*** TINY-GATE ***\n\n'
print(write.center(150))
print(conf_1)
print(conf_2)
plc_address = 0
modbus_port = 0
database_name= 'test.db'
selection = input('\n? ')

if selection == '1':
    print('\n\n********** TINY-GATE **********\n\n')
    print('**PLC**\n\n')
    plc_address  = input('IPv4 address: ')
    modbus_port = input('Modbus port:  ')
    print('\n\n**DATABASE**\n\n')
    print(conf_3)
    print(conf_4)
    selection_2= input('\n? ')

    if selection_2 == '1':
        database_name = input('database name: ')
                                                      
    if selection_2 == '2':
        remote_ip = input('Remote IPv4 address: ')
        port_n = input('Port number: ')
        database_name = input('Database nome: ')
                                                                                        
if selection == '2':
    plc_address = config['plc']['plc_address']
    modbus_port = config['plc']['modbus_port']
    database_name = config['database']['database_name']
    port_number = config['database']['port_number']
    database_number = config['database']['database_number']
    print(f'PLC_ADDRESS= {plc_address}')
    print(f'MODBUS_PORT= {modbus_port}')
    print(f'DATABASE_NAME= {database_name}')
    print(f'PORT_NUMBER= {port_number}')
    print(f'DATABASE_NUMBER= {database_number}')

# SQL fields name
fields = ("DATA0", "DATA1", "DATA2", "DATA3", "DATA4", "DATA5", "DATA6", "DATA7", "DATA8", "DATA9", "Timestamp", "Connection_State", "Error_Code") 
        
# Values array - Matrix 100 INT   
values = np.zeros(20)

#DValues array
dvalues = np.zeros(5)

# Modbus client
client = ModbusClient(plc_address, modbus_port)

# Try first socket connection
connection_state = client.connect()

# Error code 
error_code = 0
error_code_desc = ""

try:
 if(connection_state == True):
    connection_state = 1
    print("PLC connection: ONLINE")
 elif(connection_state == False):
    connection_state = 0
    print("PLC connection: OFFLINE")
except:
    connection_state = 0
    print("PLC connection: OFFLINE")


#Database connection
conn = sqlite3.connect(database_name)
cursor = conn.cursor()
print("Successfully Connected to SQLite")

#Read register each 5s
while True:
  
   # Start reading time
   startime = time.time()

   print("------------------------------------")
   timestamp = datetime.now()   
   print("Timestamp: ", timestamp)
   if(connection_state == 1):
        print("Connection state: ONLINE")
   elif(connection_state == 0):
        print("Connection state: OFFLINE")
  

   # If connection is open run modbus reading registers
   if(connection_state == 1):
    
      try: 
              # Read 20 registers - 16 int
              register = 3025 # start address
              request = client.read_holding_registers(register, 20, unit = 1)
              
              # print(request)
              
              # decode_16_bit
              index_register = 0
              index_register_modbus = 0
              
              for index_register in range (10):
              
                  temp_register_value_1 = request.registers[index_register_modbus]
                  temp_register_value_2 = request.registers[index_register_modbus + 1]
                  temp_registers = []
                  temp_registers.append(temp_register_value_1)
                  temp_registers.append(temp_register_value_2)
                  
                  decoder = BinaryPayloadDecoder.fromRegisters(temp_registers, Endian.Big, wordorder=Endian.Big)
                  values[index_register] = decoder.decode_16bit_int()
                
                  index_register_modbus += 1    
              
      except  Exception as e:
              values = np.zeros(100)
              error_code = 1
              error_code_desc = e.args[0]
              # client.close()
              connection_state = 0
              # break
        

      # Write SQL register value
      cursor.execute("INSERT INTO Matrix (" + fields[0]  + "," + fields[1]  + "," + fields[2]  + "," + fields[3]  + "," + fields[4]  + "," + fields[5]  + "," + fields[6]  + "," + fields[7]  + "," + fields[8]  + "," + fields[9] + "," + fields[10] + "," + fields[11]+ "," + fields[12] + ") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], timestamp, connection_state, error_code))
      
      # print values
      print("value 0: " + str(values[0]))
      print("value 1: " + str(values[1]))
      print("value 2: " + str(values[2]))
      print("value 3: " + str(values[3]))
      print("value 4: " + str(values[4]))
      print("value 5: " + str(values[5]))
      print("value 6: " + str(values[6]))
      print("value 7: " + str(values[7]))
      print("value 8: " + str(values[8]))
      print("value 9: " + str(values[9]))
      print("timestamp: " + str(timestamp))
      print("connection_state: " + str(connection_state))
      print("error_code: "  + str(error_code))


      # Database commit
      conn.commit()

      # End time
      endtime = time.time()
      print("Execution time: %s seconds " % (endtime - startime))
      print("Error code: ", error_code, " description: ", error_code_desc)
      time.sleep(5)
     
     
   # Else if connection is close store zeros in to dabatabase
   elif(connection_state == 0):
      
        values = np.zeros(100)
        dvalues = np.zeros(5)
        
        # Write SQL register value
        cursor.execute("INSERT INTO Matrix (" + fields[0]  + "," + fields[1]  + "," + fields[2]  + "," + fields[3]  + "," + fields[4]  + "," + fields[5]  + "," + fields[6]  + "," + fields[7]  + "," + fields[8]  + "," + fields[9] + "," + fields[10] + "," + fields[11]+ "," + fields[12] + ") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], timestamp, connection_state, error_code))          
        
        # print values
        print("field 0: " + str(values[0]))
        print("field 0: " + str(values[1]))
        print("field 0: " + str(values[2]))
        print("field 0: " + str(values[3]))
        print("field 0: " + str(values[4]))
        print("field 0: " + str(values[5]))
        print("field 0: " + str(values[6]))
        print("field 0: " + str(values[7]))
        print("field 0: " + str(values[8]))
        print("field 0: " + str(values[9]))
        print("timestamp: " + str(timestamp))
        print("connection_state: " + str(connection_state))
        print("error_code: "  + str(error_code))
        
        # Database commit
        conn.commit()
        
        # End time
        endtime = time.time()
        print("Execution time: %s seconds " % (endtime - startime))
        #  print("Error: ", error_code)
        print("Error code: ", error_code, " description: ", error_code_desc)
        connection_state = client.connect()
     
        if(connection_state == True):
           connection_state = 1
           # print("Re-Connection: ", connection_state)
           error_code = 0
           error_code_desc = ""
        elif(connection_state == False):
           connection_state = 0
           # print("Re-Connection: ", connection_state)
           error_code = 0
           error_code_desc = ""

        time.sleep(5)
