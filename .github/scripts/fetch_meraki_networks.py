import os
import requests

def fetch_meraki_networks(api_key, org_id):
    url = f"https://api.meraki.com/api/v0/organizations/{org_id}/networks"
    
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        networks = response.json()
        print(f"Organization ID: {org_id}")
        print("Networks:")
        for network in networks:
            print(f"  - {network['name']}")
    else:
        print(f"Failed to fetch networks for organization ID {org_id}")

if __name__ == "__main__":
    meraki_api_key = os.environ.get("MERAKI_API_KEY")
    org_id = os.environ.get("ORG_ID")

    if not meraki_api_key or not org_id:
        print("Meraki API key or organization ID not provided.")
    else:
        fetch_meraki_networks(meraki_api_key, org_id)
