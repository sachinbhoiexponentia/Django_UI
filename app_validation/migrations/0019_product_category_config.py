# Generated by Django 4.2.7 on 2023-12-01 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_validation', '0018_task_closure_config_closure_sql_query'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Category_Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductCategoryName', models.CharField(max_length=100)),
                ('FilterQueryOnPolicyTable', models.CharField(max_length=100)),
                ('TrainingTopics', models.CharField(max_length=100)),
                ('SellingTaskNo', models.CharField(max_length=100)),
                ('TrainingTaskNo', models.CharField(max_length=100)),
            ],
        ),
    ]
