# Generated by Django 3.1.3 on 2020-11-23 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aasrp", "0007_auto_20201123_1017"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aasrprequest",
            name="additional_info",
            field=models.TextField(blank=True, default=""),
        ),
    ]
