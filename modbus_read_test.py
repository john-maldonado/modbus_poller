from time import sleep
from pymodbus.client import ModbusSerialClient


port = 'COM14'
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
        while True:
            rr = client.read_discrete_inputs(address=0,count=3,slave=2)
            red_button = rr.bits[0]
            green_button = rr.bits[1]
            blue_button = rr.bits[2]
            print('---------------------------')
            print('Red Button {}'.format(red_button))
            print('Green Button {}'.format(green_button))
            print('Blue Button {}'.format(blue_button))
            sleep(1)
    except Exception as e:
        print(e)
        client.close()

