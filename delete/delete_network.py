import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Replace with your actual Meraki API key
# NETWORK_ID = 'N_705376291636949794'  # Dummy Network
# NETWORK_ID = os.getenv('CREATED_NETWORK_ID')  # Retrieve the value of CREATED_NETWORK_ID
NETWORK_ID_FILE = 'created_network_id.txt'  # File containing the created network ID


dashboard = meraki.DashboardAPI(API_KEY)

# Function to read the created network ID from the file
def read_created_network_id():
    try:
        with open(NETWORK_ID_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None
    
def delete_network(network_id):
    try:
        dashboard.networks.deleteNetwork(
            network_id
        )
        print(f"Network with ID {network_id} deleted successfully.")
    except meraki.APIError as e:
        print(f"Error deleting network: {e}")

if __name__ == "__main__":
    CREATED_NETWORK_ID = read_created_network_id()
    if CREATED_NETWORK_ID:
        delete_network(CREATED_NETWORK_ID)
    else:
        print("Environment variable CREATED_NETWORK_ID not set.")

