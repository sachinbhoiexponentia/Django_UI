# Generated by Django 4.2.7 on 2023-12-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_validation", "0021_alter_task_trigger_mapping_trigger_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task_trigger_mapping",
            name="Trigger",
            field=models.CharField(max_length=255, null=True),
        ),
    ]