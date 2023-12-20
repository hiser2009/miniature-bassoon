import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID
NETWORK_ID = os.getenv('NETWORK_ID')  # Replace with your actual Meraki network ID

dashboard = meraki.DashboardAPI(API_KEY)

def enable_vlans(network_id):
    try:
        response = dashboard.appliance.updateNetworkApplianceVlansSettings(network_id, vlansEnabled=True)
        print("VLANs enabled for the network:")
        print(response)
    except meraki.APIError as e:
        print(f"Error enabling VLANs: {e}")

def create_vlan(network_id, vlan_id, vlan_name, subnet, appliance_ip):
    try:
        vlan_data = {
            "id": vlan_id,
            "name": vlan_name,
            "subnet": subnet,
            "applianceIp": appliance_ip
        }

        response = dashboard.appliance.createNetworkApplianceVlan(network_id, **vlan_data)
        print(f"VLAN '{vlan_name}' created successfully:")
        print(response)
    except meraki.APIError as e:
        print(f"Error creating VLAN '{vlan_name}': {e}")

if __name__ == "__main__":
    vlan_settings = [
        {"id": 100, "name": "VLAN1", "subnet": "192.168.10.0/24", "appliance_ip": "192.168.10.1"},
        {"id": 101, "name": "VLAN2", "subnet": "192.168.20.0/24", "appliance_ip": "192.168.20.1"},
        {"id": 102, "name": "VLAN3", "subnet": "192.168.30.0/24", "appliance_ip": "192.168.30.1"},
        {"id": 103, "name": "VLAN4", "subnet": "192.168.40.0/24", "appliance_ip": "192.168.40.1"}
    ]

    enable_vlans(NETWORK_ID)

    for vlan in vlan_settings:
        create_vlan(NETWORK_ID, vlan["id"], vlan["name"], vlan["subnet"], vlan["appliance_ip"])
