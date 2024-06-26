import os
import meraki
import random
import string

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID

dashboard = meraki.DashboardAPI(API_KEY)


def create_network(org_id, network_name, network_type='combined'):
    try:
        # Remove 'DEV-' prefix if present
        if network_name.startswith('DEV-'):
            network_name = network_name[4:]

        network = dashboard.organizations.createOrganizationNetwork(
            org_id,
            name=network_name,
            productTypes=["appliance", "camera", "cellularGateway", "sensor", "switch", "wireless"],  # Update the values
            type=network_type  # Specify 'combined' as the type
        )
        network_id = network['id']
        print(f"Network '{network_name}' created successfully. Network ID: {network_id}")
        return network_id
    except meraki.APIError as e:
        print(f"Error creating network: {e}")
        return None
def create_sdwan_traffic_shaping_rule(network_id):
    try:
        # Define the traffic shaping rule parameters
        rule_params = {
            "defaultRulesEnabled": True,
            "rules": [
                {
                    "definitions": [
                        {"type": "ipRange", "value": "208.73.144.0/21"},
                        {"type": "ipRange", "value": "208.89.108.0/22"}
                    ],
                    "perClientBandwidthLimits": {"settings": "ignore"},
                    "dscpTagValue": 46,
                    "priority": "high"
                }
            ]
        }

        # Use updateNetworkApplianceTrafficShapingRules to create the rule
        response = dashboard.appliance.updateNetworkApplianceTrafficShapingRules(network_id, **rule_params)
        print("SD-WAN traffic shaping rule created successfully:")
        print(response)
    except meraki.APIError as e:
        print(f"Error creating SD-WAN traffic shaping rule: {e}")

def create_wifi_ssid(network_id, network_name):
    try:
        # Generate a random password with 13 characters
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(13))

        # Generate Wi-Fi SSID name based on the network name
        ssid_name = f"{network_name}-WiFi"

        # Define Wi-Fi SSID parameters
        ssid_params = {
            "name": ssid_name,
            "enabled": True,
            "authMode": "psk",
            "encryptionMode": "wpa",
            "psk": password,
            "minBitrate": 12,  # Recommended: 12 (for 12 Mbps)
            "bandSelection": "5 GHz band only"
        }

        # Use updateNetworkWirelessSsid to create the Wi-Fi SSID
        response = dashboard.wireless.updateNetworkWirelessSsid(network_id, number=1, **ssid_params)
        print("Wi-Fi SSID created successfully:")
        print(response)
    except meraki.APIError as e:
        print(f"Error creating Wi-Fi SSID: {e}")

if __name__ == "__main__":
    new_network_name = "TAG_CA_Branch"
    created_network_id = create_network(ORG_ID, new_network_name)

    # Set the environment variable for the created network ID
    if created_network_id:
        os.environ['CREATED_NETWORK_ID'] = created_network_id
        print(f"Environment variable CREATED_NETWORK_ID set to: {created_network_id}")

        # Write the created network ID to a file
        with open('created_network_id.txt', 'w') as file:
            file.write(created_network_id)
            print("Network ID written to file.")

        # Create SD-WAN traffic shaping rule using updateNetworkApplianceTrafficShapingRules
        create_sdwan_traffic_shaping_rule(created_network_id)

        # Create Wi-Fi SSID using updateNetworkWirelessSsid
        create_wifi_ssid(created_network_id, new_network_name)
    else:
        print("Network creation failed.")
