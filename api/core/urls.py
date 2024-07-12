from django.urls import path
from . import views

urlpatterns = [
    path('', views.SampleAPIView.as_view(), name='sample'),
    path('authorize/', views.ZohoAuthorizationView.as_view(), name='authorize'),
    path('organization/', views.ZohoOrganization.as_view(), name='organization'),
]