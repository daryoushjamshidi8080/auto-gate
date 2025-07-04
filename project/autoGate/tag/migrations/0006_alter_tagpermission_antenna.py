# Generated by Django 5.1.1 on 2025-07-01 16:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("setting", "0005_antennas_status"),
        ("tag", "0005_rename_rules_tag_rule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tagpermission",
            name="antenna",
            field=models.ManyToManyField(
                blank=True, related_name="antenna_permissions", to="setting.antennas"
            ),
        ),
    ]
