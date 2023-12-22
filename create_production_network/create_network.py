import os
import meraki

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
            productTypes=[network_type]  # Include productTypes as a list
        )
        network_id = network['id']
        print(f"Network '{network_name}' created successfully. Network ID: {network_id}")
        return network_id
    except meraki.APIError as e:
        print(f"Error creating network: {e}")
        return None

if __name__ == "__main__":
    new_network_name = "DEV-MyNewDevNet"
    created_network_id = create_network(ORG_ID, new_network_name)

    # Set the environment variable for the created network ID
    if created_network_id:
        os.environ['CREATED_NETWORK_ID'] = created_network_id
        print(f"Environment variable CREATED_NETWORK_ID set to: {created_network_id}")

        # Write the created network ID to a file
        with open('created_network_id.txt', 'w') as file:
            file.write(created_network_id)
            print("Network ID written to file.")
    else:
        print("Network creation failed.")
