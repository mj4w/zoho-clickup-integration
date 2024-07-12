from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from rest_framework import authentication, permissions
from .organization_zoho.data import *


class SampleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # print(request.user.username)
        return Response({
            'authorize-zoho': reverse('authorize', request=request)
        })
    

class ZohoAuthorizationView(APIView):
    # authentication_classes =[authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request, *args, **kwargs):
        if 'code' in request.GET:
            return self.accept_authorization(request)
        else:
            return self.authorize_zoho(request)

    def authorize_zoho(self,request):
        authorize_zoho_request = get_clean_authorization_url()
        # print(authorize_zoho_request)
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

        
        return Response(f"Code: {code}, Location: {location}, Accounts Server: {accounts_server}")

    def post(self,request, *args, **kwargs):
        return generating_tokens(request)
    
    
class ZohoOrganization(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        try:
            zoho_token = AccessTokenZoho.objects.get(user=user).access_token
            
        except AccessTokenZoho.DoesNotExist:
            return Response({
                "error": "Access token not found for the user."
            }, status.HTTP_400_BAD_REQUEST)
            
        response_data, status_code = get_organization_data(zoho_token)
        return Response(response_data, status_code)
    
    def patch(self, request, organization_id, format=None):
        user = request.user
        
        try: 
            zoho_token = AccessTokenZoho.objects.get(user=user).access_token
        except AccessTokenZoho.DoesNotExist:
            return Response({
                "error": "Access token not found for the user."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        data = request.data
        print(data)
        
        response_data, status_code = patch_organization_data(zoho_token, organization_id, data)
        if isinstance(response_data, Response):
            return response_data
        return Response(response_data, status=status_code)