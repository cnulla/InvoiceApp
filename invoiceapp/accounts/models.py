from django.db import models
from uuid import uuid4
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    )
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password
        """
        user = self._create_user(
            email,
            password = password,
            extra_fields = extra_fields
            )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email_address', max_length=255,unique=True,)
    first_name = models.CharField(verbose_name='first name',max_length=30,blank=True)
    last_name = models.CharField(verbose_name='last name',max_length=30,blank=True)

    is_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


    def generate_token(self):
        from .models import TokenGenerator
        return TokenGenerator.objects.create(user=self)


    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class TokenGenerator(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=300)
    is_used = models.BooleanField(default=False)
    date_created = models.DateField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.id:
            self.token = self.generate_token()
        return super(TokenGenerator, self).save(*args, **kwargs)


    def generate_token(self):
        return uuid4().hex

