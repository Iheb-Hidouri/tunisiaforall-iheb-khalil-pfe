# Generated by Django 4.2 on 2023-04-25 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_alter_adherent_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adherent',
            name='picture',
        ),
    ]