# Generated by Django 4.2 on 2023-04-23 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_myuser_delete_historicaladherent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]