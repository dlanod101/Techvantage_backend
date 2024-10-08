# Generated by Django 4.2.16 on 2024-10-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firebaseuser',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='firebaseuser',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='firebaseuser',
            name='photo_url',
        ),
        migrations.RemoveField(
            model_name='firebaseuser',
            name='provider_id',
        ),
        migrations.RemoveField(
            model_name='firebaseuser',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='firebaseuser',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
