import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Use your environment variable
ORG_ID = os.getenv('ORG_ID')  # Use your environment variable

dashboard = meraki.DashboardAPI(API_KEY)

# Create network
network = dashboard.organizations.createOrganizationNetwork(
    ORG_ID,
    name='Orlando_FL_Branch',
    type='combined',
    timeZone='America/New_York',
    productTypes=['appliance', 'switch', 'wireless']
)

# Extract the network ID
network_id = network['id']
print(f"Network ID: {network_id}")

# Define VLAN data
vlan_data = {
    "name": "Voice",
    "subnet": "192.168.100.0/24",
    "applianceIp": "192.168.100.1",
    "groupPolicyId": "101",
    "templateVlanType": "same",
    "cidr": "192.168.100.0/24",
    "mask": 24,
    "fixedIpAssignments": {
        "22:33:44:55:66:77": {
            "ip": "1.2.3.4",
            "name": "Some client name"
        }
    },
    "reservedIpRanges": [
        {
            "start": "192.168.1.1",
            "end": "192.168.1.100",
            "comment": "A reserved IP range"
        }
    ],
    "dnsNameservers": "google_dns",
    "dhcpHandling": "Run a DHCP server",
    "dhcpLeaseTime": "4 hours",
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
    "adaptivePolicyGroupId": "1234",
    "dhcpRelayServerIps": ["192.168.1.1/24"],
    "vpnNatSubnet": "192.168.100.0/24"
}

# Create VLAN
response_vlan = dashboard
