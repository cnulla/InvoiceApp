from django.urls import path
from invoice.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard')

]
