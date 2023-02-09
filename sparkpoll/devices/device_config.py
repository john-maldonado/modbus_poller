import json

#from sparkpoll.devices.drivers import PollerDriver

'''
class TagConfig():
    def __init__(self) -> None:
        pass

class DeviceCommConfig():
    def __init__(self) -> None:
        pass

class DeviceType():
    def __init__(self, name: str) -> None:
        if name:
            self.name = name
        else:
            raise ValueError('Invalid device type name "{}"'.format(name))
'''

# Class used to define a PollerDevice
class PollerDevice():

    # Define device types
    _device_types = [
        {
            'device_type': 'modbus/rtu',
            'comm_config': {
                'required': {
                    'port': str,
                    'baudrate': int,
                    'unit_id': int
                },
                'defaults': {
                    'bytesize': 8,
                    'startbits': 1,
                    'stopbits': 1,
                    'paritybits': 1,
                    'parity': 'E'
                }
            },
            'tag_config': {
                'required': {
                    'name': str,
                    'data_type': int,
                    'address_type': str,
                    'address': dict
                },
                'defaults': {},
                'address_types': {
                    'modbus/discrete_input': {
                        'start': int,
                        'length': int
                    },
                    'modbus/coil': {
                        'start': int,
                        'length': int
                    },
                    'modbus/input_register': {
                        'start': int,
                        'length': int
                    },
                    'modbus/holding_register': {
                        'start': int,
                        'length': int
                    }
                }
            }
        }
    ]

    # method to get set of valid device types
    def get_valid_device_types(self) -> set:
        device_types = []
        for device_type in self._device_types:
            device_types.append(device_type['device_type'])
        return set(device_types)

    # method to get a type definition by device_type name
    def get_device_type_definition(self, device_type: str) -> dict:
        definition = None
        for device_type_definition in self._device_types:
            if device_type_definition['device_type'] == device_type:
                definition = device_type_definition
        if definition:
            return definition
        else:
            raise ValueError('Invalid device type')

    # init method
    def __init__(self, device_definition: dict) -> None:

        # Base set of required keys in device definition
        required_keys = {'name', 'device_type', 'comm_config', 'tags'}
        if not required_keys.issubset(set(device_definition.keys())):
            raise ValueError(
                'Invalid device configuration, device_ definition must contain {}'.format(required_keys))

        # Set device properties
        self.name = device_definition['name']
        self.device_type = device_definition['device_type']
        self.comm_config = device_definition['comm_config']
        self.tags = device_definition['tags']

    # name property
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value:
            self._name = value
        else:
            raise ValueError('Invalid device name "{}"'.format(value))

    # device_type property
    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, value: str):
        valid_types = self.get_valid_device_types()
        if value in valid_types:
            self._device_type = value
        else:
            raise ValueError('Invalid device type "{}"'.format(value))

    # comm_config property
    @property
    def comm_config(self) -> dict:
        return self._comm_config

    @comm_config.setter
    def comm_config(self, value: dict):
        # get type definition
        type_definition = self.get_device_type_definition(self.device_type)

        # get fields for comm_config
        required = type_definition['comm_config']['required']
        defaults = type_definition['comm_config']['defaults']

        # for each field in the comm_config definition, set the comm_config field to the definition value or the default value
        config = {}
        for required_key, required_type in required.items():
            if required_key in value.keys():
                if isinstance(value[required_key], required_type):
                    config[required_key] = value[required_key]
                else:
                    raise TypeError('Value type "{req_type}" required for comm_config key "{key}" for device_type"{device_type}"'.format(
                        req_type=required_type, key=required_key, device_type=self.device_type))
            else:
                raise ValueError('comm_config key "{key}" required for device_type "{device_type}"'.format(
                    key=required_key, device_type=self.device_type))
        for default_key, default_value in defaults.items():
            if default_key in value.keys():
                if isinstance(value[default_key], type(default_value)):
                    config[default_key] = value[default_key]
                else:
                    raise TypeError('Value type "{req_type}" required for comm_config key "{key}" for device_type"{device_type}"'.format(
                        req_type=type(default_value), key=default_key, device_type=self.device_type))
            else:
                config[default_key] = default_value
        self._comm_config = config

    # tags property
    @property
    def tags(self) -> list[dict]:
        return self._tags

    @tags.setter
    def tags(self, value: list[dict]):
        # get device_type definition
        type_definition = self.get_device_type_definition(self.device_type)
        
        # get fields required for tag definition
        required = type_definition['tag_config']['required']
        defaults = type_definition['tag_config']['defaults']
        address_types = type_definition['tag_config']['address_types']


        # for each tag_definition, set the tag to the definition value or the default value
        tags = []
        for tag_definition in value:
            tag = {}
            # Check required keys
            for required_key, required_type in required.items():
                # Check if key exists
                if required_key in tag_definition.keys():
                    # Check if type matches definition type
                    if isinstance(tag_definition[required_key], required_type):
                        tag[required_key] = tag_definition[required_key]
                    else:
                        raise TypeError('Value type "{req_type}" required for tag_config key "{key}" for device_type"{device_type}"'.format(
                            req_type=required_type, key=required_key, device_type=self.device_type))
                else:
                    raise ValueError('tag_config key "{key}" required for device_type "{device_type}"'.format(
                        key=required_key, device_type=self.device_type))
            # Check keys with defaults
            for default_key, default_value in defaults.items():
                # Check if key exists
                if default_key in tag_definition.keys():
                    # Check if type matches definition type
                    if isinstance(tag_definition[default_key], type(default_value)):
                        tag[default_key] = tag_definition[default_key]
                    else:
                        raise TypeError('Value type "{req_type}" required for tag_config key "{key}" for device_type"{device_type}"'.format(
                            req_type=type(default_value), key=default_key, device_type=self.device_type))
                # else apply default value
                else:
                    tag[default_key] = default_value

            # Validate address
            address_type = tag['address_type']
            address_definition = tag['address']
            # Check if address_type is valid
            if address_type not in address_types.keys():
                raise ValueError('Invalid address type "{address_type}" for device_type "{device_type}"'.format(
                    address_type=address_type, device_type=self.device_type))
            # Get required address config for address type
            required_address_config = address_types[address_type]
            # For each key in required_address_config
            for required_address_config_key, required_address_config_type in required_address_config.items():
                # Check if required_address_key exisits
                if required_address_config_key not in address_definition:
                    raise ValueError('address_definition key "{key}" required for device_type "{device_type}"'.format(
                        key=required_address_config_key, device_type=self.device_type))
                # Check if required_address_type matches
                if required_address_config_type != type(address_definition[required_address_config_key]):
                    raise TypeError('Value type "{req_type}" required for address_definition key "{key}" for device_type"{device_type}"'.format(
                        req_type=required_address_config_type, key=required_address_config_key, device_type=self.device_type))
            # Add the tag
            tags.append(tag)
        self._tags = tags

    
    '''
    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value : PollerDriver):
    '''
        

def load_config(path: str) -> dict:
    with open(path, 'r') as f:
        config = json.load(f)
    return config

'''
configuration = load_config('./device_config.json')
myDevice = PollerDevice(configuration[0])
#print(myDevice.name)
#print(myDevice.device_type)
#print(myDevice.comm_config)
print(myDevice.tags[0])
'''
