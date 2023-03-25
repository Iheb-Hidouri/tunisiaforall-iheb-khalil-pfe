# Generated by Django 4.1.7 on 2023-03-25 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='responsablestructure',
            old_name='code_adherent',
            new_name='numero_adherent',
        ),
        migrations.RenameField(
            model_name='structure',
            old_name='code',
            new_name='code_stucture',
        ),
        migrations.RemoveField(
            model_name='adherent',
            name='numero_adherent',
        ),
        migrations.AlterField(
            model_name='adherent',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
    ]