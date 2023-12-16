import requests
import json
import os

# Replace these values with your actual Meraki API key and organization ID
meraki_api_key = os.getenv("MERAKI_API_KEY")
org_id = os.getenv("ORG_ID")
dev_network_id = "Nashville_TN_Branch"  # Manually set the value

# Create Dev network
url_create_network = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
headers = {
    "Content-Type": "application/json",
    "X-Cisco-Meraki-API-Key": meraki_api_key
}
data_create_network = {
    "name": "Dev Network",
    "type": "appliance",
    "timeZone": "America/New_York",
    "productTypes": ["appliance"]  # Add this line to specify the product type
}
response_create_network = requests.post(url_create_network, headers=headers, json=data_create_network)
print("Create Network Response:")
print(f"Status Code: {response_create_network.status_code}")
print("Response JSON:")
print(response_create_network.json())

# Create VLANs
subnets = [
    {"id": 100, "vlan_name": "Voice", "subnet": "192.168.100.0/24"},
    {"id": 200, "vlan_name": "Data", "subnet": "192.168.200.0/24"},
    {"id": 300, "vlan_name": "Infra", "subnet": "192.168.300.0/24"},
    {"id": 400, "vlan_name": "Guest", "subnet": "192.168.400.0/24"}
]
url_create_vlans = f"https://api.meraki.com/api/v1/networks/{dev_network_id}/vlans"
for subnet in subnets:
    data_create_vlan = {
        "name": subnet["vlan_name"],
        "subnet": subnet["subnet"]
    }
    response_create_vlan = requests.post(url_create_vlans, headers=headers, json=data_create_vlan)
    print(f"Create VLAN {subnet['vlan_name']} Response:")
    print(f"Status Code: {response_create_vlan.status_code}")
    print("Response JSON:")
    print(response_create_vlan.json())

# Create DHCP scopes
dhcp_scopes = [
    {"vlan_name": "Voice", "subnet": "192.168.100.0/24", "start_ip": "192.168.100.100", "end_ip": "192.168.100.200"},
    {"vlan_name": "Data", "subnet": "192.168.200.0/24", "start_ip": "192.168.200.100", "end_ip": "192.168.200.200"},
    {"vlan_name": "Infra", "subnet": "192.168.300.0/24", "start_ip": "192.168.300.100", "end_ip": "192.168.300.200"},
    {"vlan_name": "Guest", "subnet": "192.168.400.0/24", "start_ip": "192.168.400.100", "end_ip": "192.168.400.200"}
]
url_create_dhcp_scopes = f"https://api.meraki.com/api/v1/networks/{dev_network_id}/dhcp/scopes"
for scope in dhcp_scopes:
    response_create_dhcp_scope = requests.post(url_create_dhcp_scopes, headers=headers, json=scope)
    print(f"Create DHCP Scope for {scope['vlan_name']} Response:")
    print(f"Status Code: {response_create_dhcp_scope.status_code}")
    print("Response JSON:")
    print(response_create_dhcp_scope.json())

# Add additional tasks for traffic shaping rules, etc.
# ...

print("Dev deployment successful!")
