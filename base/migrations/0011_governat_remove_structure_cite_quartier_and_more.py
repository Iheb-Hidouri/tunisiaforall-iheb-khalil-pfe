# Generated by Django 4.1.7 on 2023-04-08 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_delete_delegation_delete_governat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Governat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='structure',
            name='cite_quartier',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='ville',
        ),
        migrations.CreateModel(
            name='Delegation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=2)),
                ('governat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.governat')),
            ],
        ),
        migrations.AddField(
            model_name='structure',
            name='delegation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='base.delegation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='structure',
            name='governat',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='base.governat'),
            preserve_default=False,
        ),
    ]