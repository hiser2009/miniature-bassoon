import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID
NETWORK_ID = os.getenv('CREATED_NETWORK_ID')  # Retrieve the value of CREATED_NETWORK_ID

if not NETWORK_ID:
    print("Please set the CREATED_NETWORK_ID environment variable.")
    exit()

dashboard = meraki.DashboardAPI(API_KEY)

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
    list_vlans(NETWORK_ID)
    list_dhcp_scopes(NETWORK_ID)
