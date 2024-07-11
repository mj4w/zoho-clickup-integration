from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import get_clean_authorization_url, generating_tokens
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from rest_framework import authentication, permissions


class SampleAPIView(APIView):

    def get(self, request):
        return Response(f'Hello World!')
    

class ZohoAuthorizationView(APIView):
    # authentication_classes =[authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request, *args, **kwargs):
        if 'code' in request.GET:
            return self.accept_authorization(request)
        else:
            return self.authorize_zoho(request)

    def authorize_zoho(self,request):
        authorize_zoho_request = get_clean_authorization_url()
        print(authorize_zoho_request)
        return redirect(authorize_zoho_request)

    def accept_authorization(self,request):
        code = request.GET.get('code')
        location = request.GET.get('location')
        accounts_server = request.GET.get('accounts-server')
        
        user = request.user
        try:
            user.grant_token = code
            user.location = location
            user.save()
        except User.DoesNotExist:
            return ValueError(f'User {request.user} does not exist')

        
        return HttpResponse(f"Code: {code}, Location: {location}, Accounts Server: {accounts_server}")

    def post(self,request, *args, **kwargs):
        return generating_tokens(request)