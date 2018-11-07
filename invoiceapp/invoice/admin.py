from django.contrib import admin
from invoice.models import (
    Client,
    Company,
    Invitation,
    Item,
    Invoice,
    )
# Register your models here.
admin.site.register(Client)
admin.site.register(Company)
admin.site.register(Invitation)
admin.site.register(Item)
admin.site.register(Invoice)



