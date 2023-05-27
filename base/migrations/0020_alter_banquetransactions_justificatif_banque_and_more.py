# Generated by Django 4.2 on 2023-05-27 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_adherent_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banquetransactions',
            name='justificatif_banque',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
        migrations.AlterField(
            model_name='banquetransactions',
            name='transaction_raison',
            field=models.CharField(choices=[('Don', 'Don'), ('Cotisation', 'Cotisation'), ('Frais', 'Frais'), ('Profits', 'profits')], default='don', max_length=20),
        ),
        migrations.AlterField(
            model_name='banquetransactions',
            name='transaction_type',
            field=models.CharField(choices=[('Crédit', 'Credit'), ('Débit', 'Debit')], max_length=6),
        ),
        migrations.AlterField(
            model_name='caissetransactions',
            name='justificatif_caisse',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
        migrations.AlterField(
            model_name='caissetransactions',
            name='transaction_raison',
            field=models.CharField(choices=[('Don', 'Don'), ('Cotisation', 'Cotisation'), ('Frais', 'Frais'), ('Profits', 'profits')], default='don', max_length=20),
        ),
        migrations.AlterField(
            model_name='caissetransactions',
            name='transaction_type',
            field=models.CharField(choices=[('Crédit', 'Credit'), ('Débit', 'Debit')], max_length=6),
        ),
    ]
