# Generated by Django 4.2 on 2023-05-26 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_adherent_commissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adherent',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]
