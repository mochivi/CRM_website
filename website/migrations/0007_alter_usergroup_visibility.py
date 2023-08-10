# Generated by Django 4.2.3 on 2023-08-10 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0006_alter_usergroup_records"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usergroup",
            name="visibility",
            field=models.CharField(
                choices=[("public", "Public"), ("private", "Private")],
                default="public",
                max_length=20,
            ),
        ),
    ]
