# Generated by Django 4.2 on 2023-05-03 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buy", "0002_account"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="label",
            field=models.CharField(
                choices=[("P", "New"), ("S", "Out of stock"), ("D", "Sale")],
                max_length=1,
            ),
        ),
    ]
