# Generated by Django 4.2.16 on 2024-10-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_remove_firebaseuser_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firebaseuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
