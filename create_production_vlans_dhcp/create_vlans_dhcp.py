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
        # Remove 'DEV-' prefix if present
        if vlan_name.startswith('DEV-'):
            vlan_name = vlan_name[4:]

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
            'dhcpLeaseTime': '4 hours',
            'dhcpBootOptionsEnabled': False
        }

        # Use updateNetworkApplianceVlan to create DHCP scope
        response = dashboard.appliance.updateNetworkApplianceVlan(network_id, vlan_id, **dhcp_data)
        print(f"DHCP scope for VLAN '{vlan_id}' created successfully:")
        print(response)
    except meraki.APIError as e:
        print(f"Error creating DHCP scope for VLAN '{vlan_id}': {e}")


if __name__ == "__main__":
    vlan_settings = [
        {"id": 132, "name": "VOICE", "subnet": "10.232.132.0/24", "appliance_ip": "10.232.132.1"},
        {"id": 133, "name": "DATA", "subnet": "10.232.133.0/24", "appliance_ip": "10.232.133.1"},
        {"id": 134, "name": "INFRA", "subnet": "10.232.134.0/24", "appliance_ip": "10.232.134.1"},
        {"id": 135, "name": "GUEST", "subnet": "10.232.135.0/24", "appliance_ip": "10.232.135.1"}
    ]

    enable_vlans(NETWORK_ID)

    for vlan in vlan_settings:
        create_vlan(NETWORK_ID, vlan["id"], vlan["name"], vlan["subnet"], vlan["appliance_ip"])