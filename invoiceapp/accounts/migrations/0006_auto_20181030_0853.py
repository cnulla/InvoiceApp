# Generated by Django 2.1 on 2018-10-30 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_myuser_is_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
