import requests
import json
import os

# Replace these values with your actual Meraki API key and organization ID
meraki_api_key = os.getenv("MERAKI_API_KEY")
org_id = os.getenv("ORG_ID")
dev_network_name = "Orlando_FL_Branch"  # Manually set the value

# Create Dev network
url_create_network = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
headers = {
    "Content-Type": "application/json",
    "X-Cisco-Meraki-API-Key": meraki_api_key
}
data_create_network = {
    "name": dev_network_name,
    "type": "combined",
    "timeZone": "America/New_York"
}
response_create_network = requests.post(url_create_network, headers=headers, json=data_create_network)
response_data_create_network = response_create_network.json()
print("Create Network Response:")
print(f"Status Code: {response_create_network.status_code}")
print("Response JSON:")
print(response_data_create_network)

# Extract the network ID from the response
dev_network_id = response_data_create_network.get('id')

if dev_network_id:
    print(f"Dev Network ID: {dev_network_id}")

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
    
    # Continue with other tasks...
    # ...
    
    print("Dev deployment successful!")

else:
    print("Failed to extract Dev Network ID from the response.")
