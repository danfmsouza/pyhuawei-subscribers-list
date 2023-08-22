import xml.etree.ElementTree as ET

class DeviceManager:
    @staticmethod
    def get_devices():
        tree = ET.parse('devices.xml')
        root = tree.getroot()

        devices = []
        for device in root.findall('Device'):
            device_data = {}
            for elem in device:
                device_data[elem.tag] = elem.text
            devices.append(device_data)

        return devices
