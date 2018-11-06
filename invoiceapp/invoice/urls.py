from django.urls import path
from invoice.views import (
    DashboardView,
    CreateClientView,
    ClientView,
    CreateCompanyView,
    InvitationView,
    VerifyInvitationView,
    )

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('client/', ClientView.as_view(), name='client'),
    path('create-client/', CreateClientView.as_view(), name='create-client'),
    path('create-company/', CreateCompanyView.as_view(), name='create-company'),
    path('invitation/', InvitationView.as_view(), name='invitation'),
    path('verify-invitation/', VerifyInvitationView.as_view(), name='verify-invitation'),


]
