import requests
import json
import os
import time

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

    # Create or Update VLANs
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

        # Check if the VLAN already exists by name
        url_get_vlan = f"https://api.meraki.com/api/v1/networks/{dev_network_id}/vlans"
        response_get_vlans = requests.get(url_get_vlan, headers=headers)
        existing_vlans = response_get_vlans.json()
        existing_vlan = next((vlan for vlan in existing_vlans if vlan["name"] == subnet["vlan_name"]), None)

        if existing_vlan:
            # Update the existing VLAN
            url_update_vlan = f"https://api.meraki.com/api/v1/networks/{dev_network_id}/vlans/{existing_vlan['id']}"
            response_update_vlan = requests.put(url_update_vlan, headers=headers, json=data_create_vlan)
            print(f"Update VLAN {subnet['vlan_name']} Response:")
        else:
            # Create the VLAN if it doesn't exist
            response_create_vlan = requests.post(url_create_vlans, headers=headers, json=data_create_vlan)
            print(f"Create VLAN {subnet['vlan_name']} Response:")

        print(f"Status Code: {response_create_vlan.status_code}")
        try:
            # Print the response content
            print("Response Content:")
            print(response_create_vlan.text)
            # Attempt to parse the JSON response
            print("Response JSON:")
            print(response_create_vlan.json())
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    # Continue with other tasks...
    # ...

    print("Dev deployment successful!")

else:
    print("Failed to extract Dev Network ID from the response.")
