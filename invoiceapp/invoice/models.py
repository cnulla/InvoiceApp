from django.db import models
from accounts.models import MyUser
from uuid import uuid4

# Create your models here.

class Client(models.Model):
    """ Create model for Client
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def generate_token(self):
        from invoice.models import Invitation
        return Invitation.objects.create(client=self)

    def __str__(self):
        return self.first_name


class Company(models.Model):
    """ Create company
    """
    company_name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name


class Invitation(models.Model):
    """Send Invitation to the clients
    """
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, null=True)
    is_used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        if not self.id:
            self.token = self.generate_token()
        return super(Invitation, self).save(*args, **kwargs)

    def generate_token(self):
        return uuid4().hex


class Item(models.Model):
    """ User Item model
    """
    FIXED = 'fixed'
    HOURLY = 'hourly'
    ITEM_TYPE = (
                (FIXED, 'Fixed Price'),
                (HOURLY, 'Hourly')
        )

    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    order_number = models.PositiveIntegerField(unique=True)
    order_description = models.TextField(max_length=255)
    order_date = models.DateField()
    end_date = models.DateField()
    rate = models.PositiveIntegerField(null=True)
    total_hours = models.PositiveIntegerField(null=True)
    amount = models.PositiveIntegerField(null=True)
    total_amount = models.PositiveIntegerField(null=True, blank=True, default=0)
    remarks = models.TextField(max_length=255, null=True)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE, default=FIXED)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def total(self):
        return self.rate*self.total_hours

    def __str__(self):
        return str(self.order_number)


class Invoice(models.Model):
    """ User Invoice model
    """
    FIXED = 'fixed'
    HOURLY = 'hourly'
    ORDER_TYPE = (
                (FIXED, 'Fixed Price'),
                (HOURLY, 'Hourly')
        )
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    invoice_number = models.PositiveIntegerField(unique=True)
    invoice_description = models.TextField(max_length=255)
    invoice_date = models.DateField()
    due_date = models.DateField()
    payment_status = models.BooleanField(default=False)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE, default=FIXED)
    is_draft = models.BooleanField(default=False)
    subtotal = models.PositiveIntegerField(null=True, blank=True)
    less = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    invoice_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.invoice_number)

    def total_invoice(self):
        return self.total-self.less

    def get_items(self):
        return Item.objects.filter(invoice=self)
