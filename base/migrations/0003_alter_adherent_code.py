# Generated by Django 4.2 on 2023-06-18 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_banquetransactions_raison_de_transaction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adherent',
            name='code',
            field=models.CharField(max_length=9),
        ),
    ]
