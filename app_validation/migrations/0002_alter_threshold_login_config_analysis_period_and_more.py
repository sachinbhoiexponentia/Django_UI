# Generated by Django 4.1 on 2023-11-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_validation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threshold_login_config',
            name='analysis_period',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='threshold_login_config',
            name='fls_threshold_requirement_flag',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='threshold_login_config',
            name='segment_threshold_requirement_flag',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
