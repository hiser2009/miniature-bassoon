import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID

dashboard = meraki.DashboardAPI(API_KEY)

def create_network(org_id, network_name, network_type='combined'):
    try:
        if not network_name.startswith('DEV-'):
            network_name = f'DEV-{network_name}'

        # Corrected productTypes values
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
            "name": "Allow-208.73.144.0/21-208.89.108.0/22",
            "definitions": [
                {
                    "type": "application",
                    "value": "ignore"
                },
                {
                    "type": "host",
                    "value": "208.73.144.0/21"
                },
                {
                    "type": "host",
                    "value": "208.89.108.0/22"
                }
            ],
            "perClientBandwidthLimits": {
                "settings": "ignore"
            },
            "dscpTagValue": 46,
            "priority": "high",
            "globalBandwidthLimits": {
                "limitUp": 0,
                "limitDown": 0
            }
        }

        # Use updateNetworkApplianceTrafficShaping to create the rule
        response = dashboard.appliance.updateNetworkApplianceTrafficShaping(network_id, rules=[rule_params])
        print("SD-WAN traffic shaping rule created successfully:")
        print(response)
    except meraki.APIError as e:
        print(f"Error creating SD-WAN traffic shaping rule: {e}")

if __name__ == "__main__":
    new_network_name = "LasVegas_NV_Branch"  # CREATE A NETWORK NAME
    created_network_id = create_network(ORG_ID, new_network_name)

    # Set the environment variable for the created network ID
    if created_network_id:
        os.environ['CREATED_NETWORK_ID'] = created_network_id
        print(f"Environment variable CREATED_NETWORK_ID set to: {created_network_id}")

        # Write the created network ID to a file
        with open('created_network_id.txt', 'w') as file:
            file.write(created_network_id)
            print("Network ID written to file.")

        # Create SD-WAN traffic shaping rule
        create_sdwan_traffic_shaping_rule(created_network_id)
    else:
        print("Network creation failed.")
