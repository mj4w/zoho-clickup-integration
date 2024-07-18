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
from .portal_zoho.views import *
from .project_zoho.views import *
import re
# import logging

# logger = logging.getLogger(__name__)

class SampleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # print(request.user.username)
        return Response({
            'authorize-zoho': reverse('authorize', request=request),
            'authorize-clickup': reverse('clickup-authorization', request=request)
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
    
    
class ZohoPortal(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, *args, **kwargs):
        path = request.path
        match = re.search(r'\d+', path)

        if match:
            return self.list_portal(request)
        else:
            return self.list_portal(request)
        
        
    def list_portal(self,request):
        user = request.user
        
        try:
            zoho_token = AccessTokenZoho.objects.get(user=user).access_token
            # organization, created = Organization.objects.get_or_create(user=user)
            # organization.organization_id = request.GET.get('id')
        except AccessTokenZoho.DoesNotExist:
            return {
                "error": "Access token does not exist"
            }, 500
            
        response_data, status_code = get_zoho_portal(zoho_token)
        # logger.debug(f"Organization API Response: {response_data}")
        # saving organization
        try:
            organization_id = response_data['portals'][0]['id']
            organization, created = OrganizationZoho.objects.get_or_create(user=user)
            organization.organization_id = organization_id
            organization.save()
        except Exception as e:
            return {
                "error": str(e),
            }, 500
        return Response(response_data, status_code)

    
    # def patch(self, request, organization_id, format=None):
    #     user = request.user
        
    #     try: 
    #         zoho_token = AccessTokenZoho.objects.get(user=user).access_token
    #     except AccessTokenZoho.DoesNotExist:
    #         return Response({
    #             "error": "Access token not found for the user."
    #         }, status=status.HTTP_400_BAD_REQUEST)
            
    #     data = request.data
    #     print(data)
        
    #     response_data, status_code = patch_organization_data(zoho_token, organization_id, data)
    #     if isinstance(response_data, Response):
    #         return response_data
    #     return Response(response_data, status=status_code)
    

class ZohoProjects(APIView):
    def post(self, request, *args, **kwargs):
        path = request.path
        search = re.search('projectgroups', path)
        
        if search:
            return self.post_project_group(request)
        else:
            return self.post_project(request)

    def get(self, request, *args, **kwargs):
        user = request.user
        
        try:
            zoho_token = AccessTokenZoho.objects.get(user=user).access_token
            organization_id = OrganizationZoho.objects.get(user=user).organization_id
        except (AccessTokenZoho.DoesNotExist, OrganizationZoho.DoesNotExist):
            return Response({"error": "Zoho token or Organization ID does not exist"}, status=500)
        
        response_data, status_code = list_project_data(zoho_token, organization_id)
        return Response(response_data, status=status_code)
        
    def post_project_group(self, request):
        # breakpoint()
        user = request.user
        try:
            zoho_token = AccessTokenZoho.objects.get(user=user).access_token
            organization_id = OrganizationZoho.objects.get(user=user).organization_id
        except (AccessTokenZoho.DoesNotExist, OrganizationZoho.DoesNotExist):
            return Response({"error": "Zoho Token or Organization ID does not exist"}, status=500)
        
        data = request.data
        
        print(organization_id)
        print(zoho_token)
        print(data)
        response_data, status_code = project_group(zoho_token, organization_id, data)
        if isinstance(response_data, Response):
            return response_data
        return Response(response_data, status=status_code)

    # def post(self,request, *args, **kwargs):
    #     # breakpoint()
    #     user = request.user
    #     try: 
    #         zoho_token = AccessTokenZoho.objects.get(user=user).access_token
    #         organization_id = OrganizationZoho.objects.get(user=user).organization_id
            
    #     except (AccessTokenZoho.DoesNotExist,OrganizationZoho.DoesNotExist):
    #         return Response({"error": "Zoho token or Organization ID does not exist"}, status=500)
            
    #     data = request.data
    #     response_data, status_code = create_task_data(zoho_token, organization_id, data)
    #     if isinstance(response_data, Response):
    #         return response_data
        
    #     return Response(response_data, status=status_code)
        
        
# Clickup

class ClickupAuthorization(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request, *args, **kwargs):
        if 'code' in request.GET:
            return self.get_access_token(request) 
        else:
            return self.authorization_clickup(request)
        
        
    def authorization_clickup(self,request):
        authorization_url = get_authorization_url()
        return redirect(authorization_url)
    
    def get_access_token(self,request):
        user = request.user
        code = request.GET.get('code')
        
        tokens = request_token(user,code)
        return tokens
    