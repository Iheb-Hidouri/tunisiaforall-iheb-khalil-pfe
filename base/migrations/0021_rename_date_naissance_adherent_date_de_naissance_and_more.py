# Generated by Django 4.2 on 2023-05-27 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_banquetransactions_justificatif_banque_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adherent',
            old_name='date_naissance',
            new_name='date_de_naissance',
        ),
        migrations.RenameField(
            model_name='adherent',
            old_name='lieu_naissance',
            new_name='lieu_de_naissance',
        ),
    ]
