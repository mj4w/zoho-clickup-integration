from rest_framework.response import Response
import requests
import os
from rest_framework import status
from rest_framework.renderers import JSONRenderer



def get_zoho_portal(zoho_token):
    url = "https://projectsapi.zoho.com/restapi/portals/"
    headers = {
        "Authorization": f"Zoho-oauthtoken {zoho_token}",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.HTTPError as e:
        return {"error": str(e), "response": response.text}, 500 

def patch_organization_data(zoho_token,organization_id,data):
    # breakpoint()
    url = f"https://desk.zoho.com/api/v1/organizations/{organization_id}"
    headers = {
        "Authorization": f"Zoho-oauthtoken {zoho_token}",
        "Content-Type": "application/json"
    }
    # if 'faviconURL' in data:
    #     del data['faviconURL']
    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.HTTPError as e:
        return {"error": str(e),  "response": response.text}, 422 
    