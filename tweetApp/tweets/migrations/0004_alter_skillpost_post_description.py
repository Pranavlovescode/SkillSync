# Generated by Django 5.1.4 on 2025-01-19 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tweets", "0003_alter_user_profile_photo_skillpost"),
    ]

    operations = [
        migrations.AlterField(
            model_name="skillpost",
            name="post_description",
            field=models.TextField(max_length=10000),
        ),
    ]
