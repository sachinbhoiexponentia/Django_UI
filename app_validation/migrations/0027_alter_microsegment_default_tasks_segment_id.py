# Generated by Django 4.2.7 on 2023-12-14 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_validation", "0026_alter_microsegment_default_tasks_demoseg_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="microsegment_default_tasks",
            name="Segment_id",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]