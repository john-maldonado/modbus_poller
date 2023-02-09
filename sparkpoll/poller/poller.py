from multiprocessing import Process, Queue
from sparkpoll import PollerDevice
from sparkpoll.devices import PollerDriver

class PollerProcess():
    def __init__(self, devices: list[PollerDevice], queue: Queue) -> None:
        self.devices = devices
        self.queue = queue
        self.device_type = self.devices[0].device_type
        comm_config = self.devices[0].comm_config
        self.driver = PollerDriver(device_type=self.device_type, comm_config=comm_config)
        pass

    def start(self) -> None:
        print('Process Starting')
        print(self.devices)
        print(self.queue)
        try:
            self.driver.connect()
            self.process = Process(target=self.driver.scan, args=(self.devices))
        except Exception as e:
            print(e)
        pass

    def close(self):
        pass

    
class Poller():

    def __init__(self, devices: list[PollerDevice]) -> None:
        self.devices = devices
        self.generate_processes()
        pass

    @property
    def devices(self) -> list[PollerDevice]:
        return self._devices

    @devices.setter
    def devices(self, value):
        self._devices = value

    def get_device_types(self) -> list[str]:
        device_types = []
        for device in self.devices:
            if device.device_type not in device_types:
                device_types.append(device.device_type)
        return device_types

    def get_device_type_groups(self) -> dict:
        device_type_group = {}
        for device in self.devices:
            if device.device_type not in device_type_group:
                device_type_group[device.device_type] = [device]
            else:
                device_type_group[device.device_type].append(device)
        return device_type_group
    
    def generate_processes(self):
        device_type_groups = self.get_device_type_groups()
        processes = []
        for device_type, devices in device_type_groups.items():
            if device_type == 'modbus/rtu':
                serial_port_groups = {}
                for device in devices:
                    serial_port = device.comm_config['port']
                    if serial_port not in serial_port_groups:
                        serial_port_groups[serial_port] = [device]
                    else:
                        serial_port_groups[serial_port].append(device)
                for serial_port, serial_port_group in serial_port_groups.items():
                    process_queue = Queue()
                    process = PollerProcess(serial_port_group, process_queue)
                    processes.append(process)
            else:
                raise ValueError('Unhandled device_type {}'.format(device_type))
        self.processes = processes
        pass

    def start(self):
        for process in self.processes:
            process.start()
        
        