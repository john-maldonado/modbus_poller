from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusTcpClient

from sparkpoll.devices import PollerDevice


class PollerDriver():
    def __init__(self, device_type: str, comm_config : dict) -> None:
        print('Initializing PollerDriver')
        self.device_type = device_type
        if device_type == 'modbus/rtu':
            pass
        elif device_type == 'modbus/tcp':
            pass
        else:
            raise ValueError(
                'No driver found for device type "{}"'.format(device_type))
        self.comm_config = comm_config
        print(f'PollerDriver : {self}')

    def connect(self):
        print('PollerDriver Connecting')
        print(f'PollerDriver : {self}')
        if self.device_type == 'modbus/rtu':
            print(f'device_type : {self.device_type}')
            print(f'comm_config : {self.comm_config}')
            port = self.comm_config['port']
            baudrate = self.comm_config['baudrate']
            bytesize = self.comm_config['bytesize']
            parity = self.comm_config['parity']
            stopbits = self.comm_config['stopbits']
            
            print('Creating ModbusSerialCLient')
            self.client = ModbusSerialClient(
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits)
            print(f'ModbusSerialClient : {self.client}')
            print('Connecting ModbusSerialClient')
            self.client.connect()

        else:
            raise ValueError(
                'No driver found for device type "{}"'.format(self.device_type))

    def scan(self, devices : list[PollerDevice]):
        # Very simple scan execution
        for device in devices:
            for tag in device.tags:
                name = tag['name']
                data_type = tag['data_type']
                address_type = tag['address_type']
                value = None
                if address_type == 'modbus/coil':
                        address = device['address']
                        start = address['start']
                        length = address['end']
                        res = self.client.read_coils(
                            address=start, count=length, slave=2)
                        if data_type == 11:
                            value = any(res.bits)
                if address_type == 'modbus/discrete_input':
                    address = device['address']
                    start = address['start']
                    length = address['end']
                    res = self.client.read_discrete_inputs(
                        address=start, count=length, slave=2)
                    if data_type == 11:
                        value = res.bits

                if value is not None:
                    publish_tag = {
                        'value': value,
                        'name': name,
                        'data_type': data_type,
                        'address': address,
                        'address_type': address_type,
                        'device': device.name,
                        'device_type': device.device_type
                    }
                    print('Publishing Tag')
                    print(publish_tag)
