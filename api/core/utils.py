from urllib.parse import urlencode
import os
import requests
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.shortcuts import redirect



redirect_uri = "http://localhost:8000/api/authorize/"
client_id = os.environ.get('ZOHO_CLIENT_ID')
client_secret = os.environ.get('ZOHO_CLIENT_SECRET')
url_zoho = os.environ.get('ZOHO_URL')
scope = "ZohoProjects.tasks.READ,ZohoProjects.projects.ALL,ZohoProjects.projects.READ,ZohoBugTracker.portals.READ,ZohoProjects.portals.READ"

grant_type = "authorization_code"
access_type = "online"


def get_clean_authorization_url():
    
    authorization_url = f"{url_zoho}/oauth/v2/auth?scope={scope}&client_id={client_id}&response_type=code&access_type={access_type}&redirect_uri={redirect_uri}&prompt=consent"
    
    return authorization_url

def generating_tokens(request):
    user = request.user
    if not user.is_authenticated:
        return Response("User is not authenticated", status=status.HTTP_401_UNAUTHORIZED)

    grant_token = user.grant_token
    # print(grant_token)
    try:
        response = requests.post(
            f"{url_zoho}/oauth/v2/token",
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
                zoho.scope = data['scope']
                zoho.save()
            except User.DoesNotExist:
                return ValueError(f'User {request.user} does not exist')
            return Response(data, status=status.HTTP_200_OK)
        
        else:
            return Response(data, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# clickup
clickup_client_id = os.environ.get('CLICKUP_CLIENT_ID')
clickup_client_secret = os.environ.get('CLICKUP_CLIENT_SECRET')
clickup_redirect_uri = 'http://localhost:8000/api/clickup/'

def get_authorization_url():
    authorization_url = f"https://app.clickup.com/api?client_id={clickup_client_id}&redirect_uri={clickup_redirect_uri}"
    return authorization_url
    
def request_token(user,code):
    url = "https://api.clickup.com/api/v2/oauth/token"
    try:
      response = requests.post(url, data={
        "client_id": clickup_client_id,
        "client_secret": clickup_client_secret,
        "code": code,
      })
      data = response.json()
      
      if "access_token" in data:
        try:
            clickup_token, created = AccessTokenClickup.objects.get_or_create(user=user)
            clickup_token.access_token = data['access_token']
            clickup_token.save()
        except AccessTokenClickup.DoesNotExist:
            return {"error": "Model does not exist"}
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        