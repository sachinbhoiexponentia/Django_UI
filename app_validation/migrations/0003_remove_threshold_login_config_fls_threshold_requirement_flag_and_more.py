# Generated by Django 4.1 on 2023-11-10 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_validation', '0002_alter_threshold_login_config_analysis_period_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='threshold_login_config',
            name='fls_threshold_requirement_flag',
        ),
        migrations.AddField(
            model_name='threshold_login_config',
            name='FLS_Threshold_Requirement_Flag',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
