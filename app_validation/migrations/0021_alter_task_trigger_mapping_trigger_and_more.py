# Generated by Django 4.2.7 on 2023-12-14 07:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "app_validation",
            "0020_rename_channel_subchannel_name_channel_task_mapping_subchannel_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="task_trigger_mapping",
            name="Trigger",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="threshold_logic_config",
            name="trigger_id",
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
