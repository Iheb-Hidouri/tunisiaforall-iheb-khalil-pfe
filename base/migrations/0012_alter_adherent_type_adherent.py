# Generated by Django 4.2 on 2023-05-21 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_adherent_type_document_identite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adherent',
            name='type_adherent',
            field=models.CharField(choices=[('Membre fondateur', 'Membre fondateur'), ('Membre actif', 'Membre actif'), ('Membre actif jeune', 'Membre actif jeune'), ('Soutien', 'Soutien'), ('Président', 'Président'), ('Directeur Executif', 'Directeur Executif'), ('Trésorier', 'Trésorier'), ('Simple membre', 'Simple membre')], max_length=20),
        ),
    ]