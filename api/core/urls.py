from django.urls import path
from . import views

urlpatterns = [
    path('', views.SampleAPIView.as_view(), name='sample'),
    path('authorize/', views.ZohoAuthorizationView.as_view(), name='authorize'),
    path('organization/', views.ZohoOrganization.as_view(), name='zoho-organization'),
    path('organization/<int:organization_id>/', views.ZohoOrganization.as_view(), name='zoho-organization-detail'),
    path('task/', views.ZohoTask.as_view(), name='zoho-task'),
    
    # clickup
    path('clickup/',views.ClickupAuthorization.as_view(), name='clickup-authorization'),
]