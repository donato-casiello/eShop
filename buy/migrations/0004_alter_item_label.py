# Generated by Django 4.2 on 2023-05-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buy", "0003_alter_item_label"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="label",
            field=models.CharField(
                choices=[
                    ("primary", "New"),
                    ("secondary", "Out of stock"),
                    ("danger", "Sale"),
                ],
                max_length=10,
            ),
        ),
    ]