import requests
import json
import os
import time
import meraki

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
    "timeZone": "America/New_York",
    "productTypes": ["appliance", "switch", "wireless"]
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

    # Add a delay to allow time for the network to be ready
    time.sleep(5)  # Adjust the delay time as needed

    # Use meraki library to create VLANs and DHCP scopes
    dashboard = meraki.DashboardAPI(meraki_api_key)

    subnets = [
        {"id": 100, "vlan_name": "Voice", "subnet": "192.168.100.0/24"},
        {"id": 200, "vlan_name": "Data", "subnet": "192.168.200.0/24"},
        {"id": 300, "vlan_name": "Infra", "subnet": "192.168.300.0/24"},
        {"id": 400, "vlan_name": "Guest", "subnet": "192.168.400.0/24"}
    ]

    for subnet in subnets:
        # Use the meraki library to create VLANs
        response_create_vlan = dashboard.appliance.updateNetworkApplianceVlan(
            dev_network_id,
            vlan_id='',  # Set the VLAN ID to an empty string for creation
            name=subnet["vlan_name"],
            subnet=subnet["subnet"]
            # Add other parameters as needed
        )
        print(f"Create VLAN {subnet['vlan_name']} Response:")
        print(f"Status Code: {response_create_vlan.status_code}")
        print("Response JSON:")
        print(response_create_vlan)

    # Continue with other tasks...
    # ...

    print("Dev deployment successful!")

else:
    print("Failed to extract Dev Network ID from the response.")
