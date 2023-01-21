from time import sleep
from pymodbus.client import ModbusSerialClient


port = '/dev/ttyUSB0'
baudrate = 38400
bytesize = 8
parity = 'O'
stopbits = 1

client = ModbusSerialClient(
    port=port,
    baudrate=baudrate,
    bytesize=bytesize,
    parity=parity,
    stopbits=stopbits)

client.close()

if __name__ == '__main__':
    try: 
        client.connect()
        sleep(1)
        green_start_address = 16384
        blue_start_address = 16385
        green_stop_address = 16394
        blue_stop_address = 16395
        slave = 2
        client.write_coil(green_start_address, True, slave=slave)
        sleep(1)
        client.write_coil(green_stop_address, True, slave=slave)
        sleep(1)
        client.write_coil(blue_start_address, True, slave=slave)
        sleep(1)
        client.write_coil(blue_stop_address, True, slave=slave)
        sleep(1)
        client.close()
    except Exception as e:
        print(e)
        client.close()
