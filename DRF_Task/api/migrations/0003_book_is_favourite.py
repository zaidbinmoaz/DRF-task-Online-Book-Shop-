# Generated by Django 5.0 on 2024-01-01 07:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_favourite"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="is_favourite",
            field=models.BooleanField(default=False),
        ),
    ]