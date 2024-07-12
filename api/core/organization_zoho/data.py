
import requests
import os
from rest_framework import status
def get_organization_data(zoho_token):
    headers = {
        "Authorization": f"Zoho-oauthtoken {zoho_token}"
    }
    response = requests.get(f"https://desk.zoho.com/api/v1/organizations", headers=headers)
    response.raise_for_status()
    return response.json(), response.status_code