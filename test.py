import os
import meraki

API_KEY = os.getenv('MERAKI_API_KEY')  # Use your environment variable
ORG_ID = os.getenv('ORG_ID')  # Use your environment variable

dashboard = meraki.DashboardAPI(API_KEY)

# Check if the network already exists
networks = dashboard.organizations.getOrganizationNetworks(ORG_ID)

network_name = 'Orlando_FL_Branch'
existing_network = next((n for n in networks if n['name'] == network_name), None)

if existing_network:
    # Network already exists, update VLAN
    network_id = existing_network['id']
    print(f"Network ID: {network_id}")

    vlan_data = {
        # ... VLAN data as before ...
    }
    # Enable VLANs for the network
    response_settings = dashboard.appliance.updateNetworkApplianceVlansSettings(
        network_id,
        vlansEnabled=True
    )
    # Update VLAN
    response_vlan = dashboard.appliance.updateNetworkApplianceVlan(network_id, vlan_id='100', **vlan_data)

    print("Update VLAN Response:")
    print(response_vlan)

else:
    # Network does not exist, create network and VLAN
    network = dashboard.organizations.createOrganizationNetwork(
        ORG_ID,
        name=network_name,
        type='combined',
        timeZone='America/New_York',
        productTypes=['appliance', 'switch', 'wireless']
    )

    # Extract the network ID
    network_id = network['id']
    print(f"Network ID: {network_id}")

    vlan_data = {
        # ... VLAN data as before ...
    }

    # Create VLAN
    response_vlan = dashboard.appliance.createNetworkApplianceVlan(network_id, id='100', name='voice', **vlan_data)

    print("Create VLAN Response:")
    print(response_vlan)