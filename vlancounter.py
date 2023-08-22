from vlancounter_interface import VLANCounterInterface
from device_manager import DeviceManager
import logging


class VLANCounter(VLANCounterInterface):
    def __init__(self):
        self.vlan_count = {}

    def count_vlans(self):
        devices = DeviceManager.get_devices()
        
        for device_data in devices:
            interface = device_data.get('Interface', "")
            vlan = device_data.get('Vlan')
            
            print(f"Device Data: {device_data}")
            print(f"Interface: {interface}, VLAN: {vlan}")

            if vlan in self.vlan_count:
                self.vlan_count[vlan]['count'] += 1
            else:
                self.vlan_count[vlan] = {'count': 1, 'interface': interface}

    def reset_counts(self):
        self.vlan_count = {}  # Zera os contadores

    def get_counts(self):
        return self.vlan_count