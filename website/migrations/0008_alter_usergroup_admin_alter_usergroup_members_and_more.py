# Generated by Django 4.2.3 on 2023-08-10 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("website", "0007_alter_usergroup_visibility"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usergroup",
            name="admin",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="admin_groups",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="usergroup",
            name="members",
            field=models.ManyToManyField(
                blank=True, related_name="user_groups", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="usergroup",
            name="records",
            field=models.ManyToManyField(
                blank=True, related_name="group_records", to="website.record"
            ),
        ),
    ]
