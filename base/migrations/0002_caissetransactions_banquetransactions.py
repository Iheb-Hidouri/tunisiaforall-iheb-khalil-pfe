# Generated by Django 4.2 on 2023-05-15 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaisseTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('entreprise', models.CharField(max_length=50)),
                ('libelle', models.CharField(max_length=50)),
                ('recu_numero', models.CharField(max_length=20)),
                ('debit', models.BooleanField(default=False)),
                ('credit', models.BooleanField(default=False)),
                ('solde', models.DecimalField(decimal_places=2, max_digits=10)),
                ('justificatif_caisse', models.ImageField(blank=True, null=True, upload_to='')),
                ('adherent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.adherent')),
                ('evenement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.evenement')),
                ('structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.structure')),
            ],
        ),
        migrations.CreateModel(
            name='BanqueTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('entreprise', models.CharField(max_length=50)),
                ('libelle', models.CharField(max_length=50)),
                ('banque', models.CharField(max_length=50)),
                ('cheque_numero', models.CharField(max_length=20)),
                ('debit', models.BooleanField(default=False)),
                ('credit', models.BooleanField(default=False)),
                ('solde', models.DecimalField(decimal_places=2, max_digits=10)),
                ('justificatif_banque', models.ImageField(blank=True, null=True, upload_to='')),
                ('adherent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.adherent')),
                ('evenement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.evenement')),
                ('structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.structure')),
            ],
        ),
    ]
