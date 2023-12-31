# Generated by Django 4.1 on 2023-11-17 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_validation', '0012_alter_allocation_parameters_xx_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation_parameters',
            name='Buffer_Days',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocation_parameters',
            name='DemoSeg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocation_parameters',
            name='Due_Days',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocation_parameters',
            name='PricePoint_Reward',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocation_parameters',
            name='Segment_id',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocation_parameters',
            name='ValueSeg',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
