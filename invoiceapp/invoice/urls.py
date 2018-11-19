from django.urls import path
from invoice.views import (
    DashboardView,
    CreateClientView,
    ClientView,
    CreateCompanyView,
    CreateInvoiceView,
    ItemFormView,
    InvoiceListView,
    InvoiceDetailView,
    UpdateInvoiceView
    )

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('client/', ClientView.as_view(), name='client'),
    path('create-client/', CreateClientView.as_view(), name='create-client'),
    path('create-company/', CreateCompanyView.as_view(), name='create-company'),
    path('create-invoice/', CreateInvoiceView.as_view(), name='create-invoice'),
    path('add/item/', ItemFormView.as_view(), name='item-form'),
    path('invoice/', InvoiceListView.as_view(), name='invoice'),
    path('invoice-detail/<int:id>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('update-invoice/<int:id>/', UpdateInvoiceView.as_view(), name='update-invoice')

]
