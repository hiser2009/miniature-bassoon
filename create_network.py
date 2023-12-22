import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID

dashboard = meraki.DashboardAPI(API_KEY)

def create_network(org_id, network_name, network_type='appliance'):
    try:
        network = dashboard.organizations.createOrganizationNetwork(
            org_id,
            name=network_name,
            type=network_type
        )
        print(f"Network '{network_name}' created successfully. Network ID: {network['id']}")
    except meraki.APIError as e:
        print(f"Error creating network: {e}")

if __name__ == "__main__":
    new_network_name = "MyNewDevNet"
    create_network(ORG_ID, new_network_name)
