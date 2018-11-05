from django.contrib import admin
from invoice.models import Client, Company, Invitation

# Register your models here.
admin.site.register(Client)
admin.site.register(Company)
admin.site.register(Invitation)

