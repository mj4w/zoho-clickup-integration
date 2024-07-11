from urllib.parse import urlencode
import os
import requests
from rest_framework.response import Response
from rest_framework import status

redirect_uri = "http://localhost:8000/authorize/"
client_id = os.environ.get('ZOHO_CLIENT_ID')
client_secret = os.environ.get('ZOHO_CLIENT_SECRET')
scope = "Desk.tickets.READ,Desk.basic.READ"
grant_type = "authorization_code"


def get_clean_authorization_url():
    authorization_url = f"https://accounts.zoho.com/oauth/v2/auth?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&state=5466400890088961855"
    
    return authorization_url

def generating_tokens(request):
    user = request.user
    if not user.is_authenticated:
        return Response("User is not authenticated", status=status.HTTP_401_UNAUTHORIZED)

    grant_token = user.grant_token
    # print(grant_token)
    try:
        response = requests.post(
            "https://accounts.zoho.com/oauth/v2/token",
            data={
                "code": grant_token,
                "grant_type": grant_type,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri
            }
        )
        data = response.json()
        if 'access_token' in data:
            return Response(data, status=status.HTTP_200_OK)
        
        else:
            return Response(data, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)