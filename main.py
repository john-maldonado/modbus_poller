import sparkpoll

device_config_path = './device_config.json'
device_configs = sparkpoll.load_config(device_config_path)

myDevice = sparkpoll.PollerDevice(device_configs[0])

print(myDevice.tags)
