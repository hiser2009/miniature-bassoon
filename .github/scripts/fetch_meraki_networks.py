import requests
import os

def fetch_meraki_networks(api_key):
    url = "https://api.meraki.com/api/v0/organizations"
    
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        organizations = response.json()
        for org in organizations:
            org_id = org["id"]
            org_name = org["name"]
            
            networks_url = f"https://api.meraki.com/api/v0/organizations/{org_id}/networks"
            networks_response = requests.get(networks_url, headers=headers)

            if networks_response.status_code == 200:
                networks = networks_response.json()
                print(f"Organization: {org_name}")
                print("Networks:")
                for network in networks:
                    print(f"  - {network['name']}")
            else:
                print(f"Failed to fetch networks for organization {org_name}")

    else:
        print("Failed to fetch organizations")

if __name__ == "__main__":
    meraki_api_key = os.environ.get("MERAKI_API_KEY")
    if meraki_api_key:
        fetch_meraki_networks(meraki_api_key)
    else:
        print("Meraki API key not provided.")
