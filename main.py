import requests
from requests.auth import HTTPBasicAuth

# Zendesk API credentials and endpoints
ZENDESK_SUBDOMAIN = 'your_subdomain'
ZENDESK_EMAIL = 'your_email/token'
ZENDESK_API_TOKEN = 'your_api_token'
ZENDESK_API_URL = f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2'

# List of numbers to search for in the 'PO #/ITO #' field
numbers_list = ['12345', '67890', '11223']

# Headers for the Zendesk API request
headers = {
    'Content-Type': 'application/json'
}

# Authenticate
auth = HTTPBasicAuth(ZENDESK_EMAIL, ZENDESK_API_TOKEN)

# The custom field ID for 'PO #/ITO #' (replace this with your actual field ID)
PO_ITO_CUSTOM_FIELD_ID = 'your_custom_field_id'

def search_and_update_tickets():
    for number in numbers_list:
        # Search for tickets
        search_url = f"{ZENDESK_API_URL}/search.json?query=type:ticket"
        
        response = requests.get(search_url, headers=headers, auth=auth)
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            for ticket in results:
                # Check if the ticket has the 'PO #/ITO #' field with the searched number
                custom_fields = ticket.get('custom_fields', [])
                po_ito_field = next((field for field in custom_fields if field['id'] == PO_ITO_CUSTOM_FIELD_ID), None)
                
                if po_ito_field and po_ito_field['value'] == number:
                    # Update ticket status to 'pending'
                    ticket_id = ticket['id']
                    update_url = f"{ZENDESK_API_URL}/tickets/{ticket_id}.json"
                    update_data = {
                        "ticket": {
                            "status": "pending"
                        }
                    }
                    
                    # Make the PUT request to update the ticket
                    update_response = requests.put(update_url, json=update_data, headers=headers, auth=auth)
                    
                    if update_response.status_code == 200:
                        print(f"Ticket {ticket_id} updated to pending.")
                    else:
                        print(f"Failed to update ticket {ticket_id}.")
        else:
            print(f"Failed to search tickets. Status Code: {response.status_code}")

# Run the function to search and update tickets
search_and_update_tickets()
