# Generated by Django 4.1.7 on 2023-04-19 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_adherent_structure_alter_structure_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdherentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Adherent created'), ('update', 'Adherent updated'), ('delete', 'Adherent deleted')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField()),
                ('adherent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.adherent')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]