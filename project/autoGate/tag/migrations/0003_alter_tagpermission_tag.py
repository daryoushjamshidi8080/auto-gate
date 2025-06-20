# Generated by Django 5.1.1 on 2025-06-07 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tag", "0002_tagpermission"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tagpermission",
            name="tag",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tag_permissions",
                to="tag.tag",
            ),
        ),
    ]
