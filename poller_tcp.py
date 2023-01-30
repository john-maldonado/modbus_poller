from pymodbus.client import ModbusTcpClient
from datetime import datetime
import time

class ModbusData:
    def __init__(self):
        self.data = {}

    def update_data(self, new_data):
        self.data = new_data

def modbus_poll(ip, port, modbus_data):
    client = ModbusTcpClient(ip, port)
    while True:
        # Connect to the Modbus device
        connection = client.connect()
        if connection:
            # Read holding registers
            result = client.read_holding_registers(0, 10, unit=1)
            if result.isError():
                print("Error reading holding registers")
            else:
                modbus_data.update_data(result.registers)
                print(f'Data updated at {datetime.now()}')
        else:
            print("Error connecting to device")
        # Close the connection
        client.close()
        # Sleep for a certain period of time before polling again
        time.sleep(30)

if __name__ == '__main__':
    modbus_data = ModbusData()
    modbus_poll('192.168.1.1', 502, modbus_data)
