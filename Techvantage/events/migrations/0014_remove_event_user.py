# Generated by Django 4.2.16 on 2024-10-03 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_remove_event_author_event_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
    ]
