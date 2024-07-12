from urllib.parse import urlencode
import os
import requests
from rest_framework.response import Response
from rest_framework import status
from .models import User, AccessTokenZoho

redirect_uri = "http://localhost:8000/authorize/"
client_id = os.environ.get('ZOHO_CLIENT_ID')
client_secret = os.environ.get('ZOHO_CLIENT_SECRET')
url_zoho = os.environ.get('ZOHO_URL')
# scope = "Desk.settings.READ,Desk.basic.READ"
grant_type = "authorization_code"


def get_clean_authorization_url(scope):
    authorization_url = f"{url_zoho}/oauth/v2/auth?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&state=5466400890088961855"
    
    return authorization_url

def generating_tokens(request):
    user = request.user
    if not user.is_authenticated:
        return Response("User is not authenticated", status=status.HTTP_401_UNAUTHORIZED)

    grant_token = user.grant_token
    # print(grant_token)
    try:
        response = requests.post(
            "{url_zoho}/oauth/v2/token",
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
            user = request.user
            try:
                zoho, created = AccessTokenZoho.objects.get_or_create(user=user)
                zoho.access_token = data['access_token']
                zoho.save()
            except User.DoesNotExist:
                return ValueError(f'User {request.user} does not exist')
            return Response(data, status=status.HTTP_200_OK)
        
        else:
            return Response(data, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)