# Generated by Django 4.1 on 2023-11-17 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_validation', '0006_allocation_parameters_channel_task_mapping_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_trigger_mapping',
            name='Task_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
