# Generated by Django 4.2.7 on 2023-12-14 08:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_validation", "0023_alter_trigger_on_query_trigger_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="allocation_parameters",
            name="DemoSeg",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
