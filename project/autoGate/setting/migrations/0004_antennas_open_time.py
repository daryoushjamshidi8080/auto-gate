# Generated by Django 5.1.1 on 2025-06-02 16:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("setting", "0003_alter_antennas_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="antennas",
            name="open_time",
            field=models.IntegerField(default=30),
        ),
    ]
