# Generated by Django 4.2 on 2023-05-27 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_rename_email_adherent_adresse_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='structure',
            old_name='email',
            new_name='adresse_email',
        ),
        migrations.RenameField(
            model_name='structure',
            old_name='date_creation',
            new_name='date_de_création',
        ),
        migrations.RenameField(
            model_name='structure',
            old_name='delegation',
            new_name='délégation',
        ),
        migrations.RenameField(
            model_name='structure',
            old_name='governat',
            new_name='gouvernorat',
        ),
        migrations.RenameField(
            model_name='structure',
            old_name='libelle',
            new_name='libellé',
        ),
        migrations.RenameField(
            model_name='structure',
            old_name='telephone',
            new_name='numéro_de_téléphone',
        ),
    ]