from multiprocessing import Process, Queue
from pymodbus.client import ModbusSerialClient as ModbusClient
import time

from sparkpoll import PollerDevice, load_config


def modbus_poller(queue):
    # Code to periodically poll devices using modbus-rtu
    port = '/dev/ttyUSB0'
    baudrate = 38400
    bytesize = 8
    parity = 'O'
    stopbits = 1

    client = ModbusClient(
        port=port,
        baudrate=baudrate,
        bytesize=bytesize,
        parity=parity,
        stopbits=stopbits)
    
    client.connect()

    while True:
        result = client.read_discrete_inputs(address=0, count=3, slave=2)
        red_button = result.bits[0]
        green_button = result.bits[1]
        blue_button = result.bits[2]
        data = {
            'red_button': red_button,
            'green_button': green_button,
            'blue_button': blue_button
        }
        queue.put(data)
        time.sleep(5)
    client.close()


def set_function(data):
    # Code to perform set function on data
    print(data)
    pass


def data_consumer(queue):
    while True:
        data = queue.get()
        set_function(data)


if __name__ == '__main__':
    queue = Queue()
    modbus_poller_process = Process(target=modbus_poller, args=(queue,))
    data_consumer_process = Process(target=data_consumer, args=(queue,))
    modbus_poller_process.start()
    data_consumer_process.start()
