import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID
NETWORK_ID_FILE = 'created_network_id.txt'  # File containing the created network ID

dashboard = meraki.DashboardAPI(API_KEY)

# Function to read the created network ID from the file
def read_created_network_id():
    try:
        with open(NETWORK_ID_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def enable_vlans(network_id):
    try:
        response = dashboard.appliance.updateNetworkApplianceVlansSettings(network_id, vlansEnabled=True)
        print("VLANs enabled for the network:")
        print(response)
    except meraki.APIError as e:
        print(f"Error enabling VLANs: {e}")

def create_vlan(network_id, vlan_id, vlan_name, subnet, appliance_ip):
    try:
        # Ensure the VLAN name is prefixed with 'DEV-'
        if not vlan_name.startswith('DEV-'):
            vlan_name = f'DEV-{vlan_name}'

        vlan_data = {
            "id": vlan_id,
            "name": vlan_name,
            "subnet": subnet,
            "applianceIp": appliance_ip,
            # "dhcpHandling": "Run a DHCP server"  # Enable DHCP
        }

        response = dashboard.appliance.createNetworkApplianceVlan(network_id, **vlan_data)
        print(f"VLAN '{vlan_name}' created successfully:")
        print(response)

        # Create DHCP scope for the VLAN
        create_dhcp_scope(network_id, vlan_id, subnet)
    except meraki.APIError as e:
        print(f"Error creating VLAN '{vlan_name}': {e}")

def create_dhcp_scope(network_id, vlan_id, subnet):
    try:
        dhcp_data = {
            "subnet": subnet,
            "applianceIp": f"{subnet.split('.')[0]}.{subnet.split('.')[1]}.{vlan_id}.1",
            "minIpAddress": f"{subnet.split('.')[0]}.{subnet.split('.')[1]}.{vlan_id}.100",
            "maxIpAddress": f"{subnet.split('.')[0]}.{subnet.split('.')[1]}.{vlan_id}.254",
            "defaultGateway": f"{subnet.split('.')[0]}.{subnet.split('.')[1]}.{vlan_id}.1",
            "dnsNameservers": "upstream_dns",
            'dhcpHandling': 'Run a DHCP server',
            'dhcpLeaseTime': '12 hours',
            'dhcpBootOptionsEnabled': False
        }

        # Use updateNetworkApplianceVlan to create DHCP scope
        response = dashboard.appliance.updateNetworkApplianceVlan(network_id, vlan_id, **dhcp_data)
        print(f"DHCP scope for VLAN '{vlan_id}' created successfully:")
        print(response)
    except meraki.APIError as e:
        print(f"Error creating DHCP scope for VLAN '{vlan_id}': {e}")

if __name__ == "__main__":
    # Retrieve the created network ID from the file
    CREATED_NETWORK_ID = read_created_network_id()
    if CREATED_NETWORK_ID:
        enable_vlans(CREATED_NETWORK_ID)

        vlan_settings = [
            {"id": 136, "name": "VOICE", "subnet": "10.232.136.0/24", "appliance_ip": "10.232.136.1"},
            {"id": 137, "name": "DATA", "subnet": "10.232.137.0/24", "appliance_ip": "10.232.137.1"},
            {"id": 138, "name": "INFRA", "subnet": "10.232.138.0/24", "appliance_ip": "10.232.138.1"},
            {"id": 139, "name": "GUEST", "subnet": "10.232.139.0/24", "appliance_ip": "10.232.139.1"}
        ]

        for vlan in vlan_settings:
            create_vlan(CREATED_NETWORK_ID, vlan["id"], vlan["name"], vlan["subnet"], vlan["appliance_ip"])
    else:
        print("Environment variable CREATED_NETWORK_ID not set.")
