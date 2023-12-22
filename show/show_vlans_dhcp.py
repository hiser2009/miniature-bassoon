import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID
# NETWORK_ID_FILE = 'created_network_id.txt'  # File containing the created network ID
NETWORK_ID_FILE = 'created_network_id.txt'  # File containing the created network ID


dashboard = meraki.DashboardAPI(API_KEY)

# Function to read the created network ID from the file
def read_created_network_id():
    try:
        with open(NETWORK_ID_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def list_vlans(network_id):
    try:
        vlans = dashboard.appliance.getNetworkApplianceVlans(network_id)
        print("VLANs on the network:")
        for vlan in vlans:
            print(f"VLAN ID: {vlan['id']}, Name: {vlan['name']}, Subnet: {vlan['subnet']}")
    except meraki.APIError as e:
        print(f"Error listing VLANs: {e}")

def list_dhcp_scopes(network_id):
    try:
        dhcp_scopes = dashboard.appliance.getNetworkApplianceVlans(network_id)
        print("DHCP Scopes on the network:")
        for dhcp_scope in dhcp_scopes:
            print(f"VLAN ID: {dhcp_scope['id']}, Subnet: {dhcp_scope['subnet']}")
    except meraki.APIError as e:
        print(f"Error listing DHCP scopes: {e}")

if __name__ == "__main__":
    # Retrieve the created network ID from the file
    CREATED_NETWORK_ID = read_created_network_id()
    if CREATED_NETWORK_ID:
        list_vlans(CREATED_NETWORK_ID)
        list_dhcp_scopes(CREATED_NETWORK_ID)

    else:
        print("Environment variable CREATED_NETWORK_ID not set.")

