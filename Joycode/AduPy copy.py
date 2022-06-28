# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM7', baudrate=9600)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

weight = []
def measure():
  while True:
   if arduino.in_waiting:
        packet = arduino.readline()
        print(int(packet.decode('utf')))
        if int(packet.decode('utf')) != 0:
                  weight.append(int(packet.decode('utf')))
        if int(packet.decode('utf')) > 2000 and int(packet.decode('utf')) != 0:
                 con = input("Do you want to con? Y/N:")
                 write_read(con)
                 if con == "N":
                   print(max(set(weight), key = weight.count))
                   exit()
                 else:
                  continue

measure()



   