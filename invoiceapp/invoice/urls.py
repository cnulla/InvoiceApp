from django.urls import path
from invoice.views import (
    DashboardView,
    CreateClientView,
    ClientView,
    )

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('client/', ClientView.as_view(), name='client'),
    path('create-client/', CreateClientView.as_view(), name='create-client'),

]
