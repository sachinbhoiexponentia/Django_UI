# Generated by Django 4.2.7 on 2023-12-14 08:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_validation", "0025_alter_allocation_parameters_valueseg"),
    ]

    operations = [
        migrations.AlterField(
            model_name="microsegment_default_tasks",
            name="DemoSeg",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="microsegment_default_tasks",
            name="ValueSeg",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
