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

    # Use requests library to create VLANs and DHCP scopes
    url_create_vlans = f"https://api.meraki.com/api/v1/networks/{dev_network_id}/vlans"
    payload_vlans = {
        "name": "My VLAN",
        "subnet": "192.168.1.0/24",
        "applianceIp": "192.168.1.2",
        "groupPolicyId": "101",
        "templateVlanType": "same",
        "cidr": "192.168.1.0/24",
        "mask": 28,
        "fixedIpAssignments": {
            "22:33:44:55:66:77": {
                "ip": "1.2.3.4",
                "name": "Some client name"
            }
        },
        "reservedIpRanges": [
            {
                "start": "192.168.1.0",
                "end": "192.168.1.1",
                "comment": "A reserved IP range"
            }
        ],
        "dnsNameservers": "google_dns",
        "dhcpHandling": "Run a DHCP server",
        "dhcpLeaseTime": "1 day",
        "dhcpBootOptionsEnabled": False,
        "dhcpBootNextServer": "1.2.3.4",
        "dhcpBootFilename": "sample.file",
        "dhcpOptions": [
            {
                "code": "5",
                "type": "text",
                "value": "five"
            }
        ],
        "ipv6": {
            "enabled": True,
            "prefixAssignments": [
                {
                    "autonomous": False,
                    "staticPrefix": "2001:db8:3c4d:15::/64",
                    "staticApplianceIp6": "2001:db8:3c4d:15::1",
                    "origin": {
                        "type": "internet",
                        "interfaces": ["wan0"]
                    }
                }
            ]
        },
        "mandatoryDhcp": {"enabled": True},
        "adaptivePolicyGroupId": "1234",
        "dhcpRelayServerIps": [
            "192.168.1.0/24",
            "192.168.128.0/24"
        ],
        "vpnNatSubnet": "192.168.1.0/24"
    }

    headers_vlans = {
        "Authorization": f"Bearer {meraki_api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response_vlans = requests.post(url_create_vlans, headers=headers_vlans, json=payload_vlans)
    print("Create VLANs Response:")
    print(f"Status Code: {response_vlans.status_code}")
    print("Response JSON:")
    print(response_vlans.text.encode('utf8'))

    # Continue with other tasks...
    # ...

    print("Dev deployment successful!")

else:
    print("Failed to extract Dev Network ID from the response.")
