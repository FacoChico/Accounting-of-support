# Generated by Django 5.0.6 on 2024-05-12 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("logistics", "0003_remove_logistics_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
        migrations.AlterModelOptions(
            name="logistics",
            options={"verbose_name": "Logistics", "verbose_name_plural": "Logistics"},
        ),
    ]
