import logging

import serial.tools.list_ports as list_ports
import serial as serial

ports = list_ports.comports()
for port in ports:
    print(port.device)
    print(port.description)

try:
    ser = serial.Serial("COM3", 9600)
    while True:
        input_data = input("Enter your data: ")
        ser.write(input_data.encode())
        print(f"Data sent: {input_data}")
except Exception as err:
    logging.error("port error : {}".format(err))


