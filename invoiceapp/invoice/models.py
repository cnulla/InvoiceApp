from django.db import models

# Create your models here.

class Client(models.Model):
    """ Create model for Client
    """

    company = models.ForeignKey('Company', on_delete=models.CASCADE)
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
    is_used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=300)


    def save(self, *args, **kwargs):
        if not self.id:
            self.token = self.generate_token()
        return super(TokenGenerator, self).save(*args, **kwargs)


    def generate_token(self):
        return uuid4().hex
