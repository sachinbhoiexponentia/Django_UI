# Generated by Django 4.2.7 on 2023-12-14 07:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_validation", "0022_alter_task_trigger_mapping_trigger"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trigger_on_query",
            name="Trigger_id",
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
