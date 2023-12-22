import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID
NETWORK_ID = os.getenv('NETWORK_ID')  # Replace with your actual Meraki network ID

dashboard = meraki.DashboardAPI(API_KEY)

def list_vlans(network_id):
    try:
        vlans = dashboard.appliance.getNetworkApplianceVlans(network_id)
        print("VLANs on the network:")
        for vlan in vlans:
            print(f"VLAN ID: {vlan['id']}, Name: {vlan['name']}, Subnet: {vlan['subnet']}")
        return vlans
    except meraki.APIError as e:
        print(f"Error listing VLANs: {e}")
        return []

def list_dhcp_scopes(network_id):
    try:
        dhcp_scopes = dashboard.appliance.getNetworkApplianceVlans(network_id)
        print("DHCP Scopes on the network:")
        for dhcp_scope in dhcp_scopes:
            print(f"VLAN ID: {dhcp_scope['id']}, Subnet: {dhcp_scope['subnet']}")
        return dhcp_scopes
    except meraki.APIError as e:
        print(f"Error listing DHCP scopes: {e}")
        return []

def delete_vlan(network_id, vlan_id):
    try:
        response = dashboard.appliance.deleteNetworkApplianceVlan(network_id, vlan_id)
        print(f"VLAN ID {vlan_id} deleted successfully.")
        print(response)
    except meraki.APIError as e:
        print(f"Error deleting VLAN ID {vlan_id}: {e}")

if __name__ == "__main__":
    vlans = list_vlans(NETWORK_ID)
    dhcp_scopes = list_dhcp_scopes(NETWORK_ID)

    for vlan in vlans:
        if vlan['id'] != 1:
            delete_vlan(NETWORK_ID, vlan['id'])
