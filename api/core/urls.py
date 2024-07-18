from django.urls import path
from . import views

urlpatterns = [
    path('', views.SampleAPIView.as_view(), name='sample'),
    path('authorize/', views.ZohoAuthorizationView.as_view(), name='authorize'),
    path('portal/', views.ZohoPortal.as_view(), name='zoho-portal'),
    path('portal/<int:organization_id>/', views.ZohoPortal.as_view(), name='zoho-portal-detail'),
    path('project/list/', views.ZohoProjects.as_view(), name='zoho-project'),
    
    #post
    path('projectgroups/create/', views.ZohoProjects.as_view(), name='zoho-projectgroups'),
    
    # clickup
    path('clickup/',views.ClickupAuthorization.as_view(), name='clickup-authorization'),
]