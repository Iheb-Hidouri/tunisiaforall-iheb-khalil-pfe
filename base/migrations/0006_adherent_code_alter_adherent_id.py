# Generated by Django 4.1.7 on 2023-04-01 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_code_adherent_responsablestructure_numero_adherent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adherent',
            name='code',
            field=models.CharField(default=0, max_length=8, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adherent',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]