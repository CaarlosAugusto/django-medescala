# Generated by Django 5.1.6 on 2025-03-03 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("escala_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]
