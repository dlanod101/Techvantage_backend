# Generated by Django 4.2.16 on 2024-10-03 20:04

from django.db import migrations, models
import django.db.models.deletion
import jobs.models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='user',
            field=models.ForeignKey(default=jobs.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, related_name='job', to='authapp.firebaseuser'),
        ),
    ]
