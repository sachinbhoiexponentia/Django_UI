# Generated by Django 4.1 on 2023-11-17 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_validation', '0014_alter_product_mix_focus_demoseg_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product_mix_focus',
            unique_together={('Channel', 'Subchannel', 'DemoSeg', 'ValueSeg', 'Focus_Product')},
        ),
    ]
