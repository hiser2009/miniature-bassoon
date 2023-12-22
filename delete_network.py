import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
ORG_ID = os.getenv('ORG_ID')  # Replace with your actual Meraki organization ID
NETWORK_ID = os.getenv('N_705376291636949792')  # MyNewDevNet 

dashboard = meraki.DashboardAPI(API_KEY)

def delete_network(org_id, network_id):
    try:
        dashboard.organizations.deleteOrganizationNetwork(
            org_id,
            network_id
        )
        print(f"Network with ID {network_id} deleted successfully.")
    except meraki.APIError as e:
        print(f"Error deleting network: {e}")

if __name__ == "__main__":
    delete_network(ORG_ID, NETWORK_ID)
