import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID
NETWORK_ID = os.getenv('NETWORK_ID')  # Replace with your actual Meraki network ID

dashboard = meraki.DashboardAPI(API_KEY)

def create_vlan(network_id, vlan_id, vlan_name, subnet, appliance_ip):
    try:
        vlan_data = {
            "id": vlan_id,
            "name": vlan_name,
            "subnet": subnet,
            "applianceIp": appliance_ip
        }

        response = dashboard.appliance.createNetworkApplianceVlan(network_id, **vlan_data)
        print("VLAN created successfully:")
        print(response)
    except meraki.APIError as e:
        print(f"Error creating VLAN: {e}")

if __name__ == "__main__":
    vlan_id = input("Enter VLAN ID: ")
    vlan_name = input("Enter VLAN Name: ")
    subnet = input("Enter VLAN Subnet (e.g., 192.168.10.0/24): ")
    appliance_ip = input("Enter Appliance IP Address: ")

    create_vlan(NETWORK_ID, vlan_id, vlan_name, subnet, appliance_ip)
