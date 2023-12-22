import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
NETWORK_ID = 'N_705376291636949793'  # MyNewDevNet Meraki network ID N_705376291636949793

dashboard = meraki.DashboardAPI(API_KEY)

def delete_network(network_id):
    try:
        dashboard.networks.deleteNetwork(
            network_id
        )
        print(f"Network with ID {network_id} deleted successfully.")
    except meraki.APIError as e:
        print(f"Error deleting network: {e}")

if __name__ == "__main__":
    delete_network(NETWORK_ID)
