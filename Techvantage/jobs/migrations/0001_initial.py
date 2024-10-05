# Generated by Django 4.2.16 on 2024-09-28 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('job_type', models.CharField(default='general', max_length=255)),
                ('location', models.CharField(default='general', max_length=255)),
                ('experience', models.CharField(default='general', max_length=255)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
