# Generated by Django 4.2 on 2023-05-31 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_alter_banquetransactions_raison_de_transaction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banquetransactions',
            name='type_de_transaction',
            field=models.CharField(choices=[('Crédit', 'Crédit'), ('Débit', 'Débit')], max_length=6),
        ),
        migrations.AlterField(
            model_name='caissetransactions',
            name='type_de_transaction',
            field=models.CharField(choices=[('Crédit', 'Crédit'), ('Débit', 'Débit')], max_length=6),
        ),
        migrations.AlterField(
            model_name='cotisation',
            name='type_de_cotisation',
            field=models.CharField(choices=[('B', 'Banque'), ('C', 'Caisse')], max_length=1),
        ),
    ]
