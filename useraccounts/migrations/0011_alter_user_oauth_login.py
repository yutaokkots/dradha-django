# Generated by Django 4.2.7 on 2023-12-08 06:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("useraccounts", "0010_alter_user_avatar_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="oauth_login",
            field=models.CharField(default="None", max_length=20, unique=True),
        ),
    ]
