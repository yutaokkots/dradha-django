# Generated by Django 4.2.7 on 2023-12-04 07:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("useraccounts", "0004_user_avatar_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="oauth_login",
            field=models.BooleanField(default=False),
        ),
    ]