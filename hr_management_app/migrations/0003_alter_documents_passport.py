# Generated by Django 4.2 on 2023-08-25 10:28

from django.db import migrations, models
import hr_management_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_management_app', '0002_employeeleave_code_executed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='passport',
            field=models.FileField(blank=True, null=True, upload_to=hr_management_app.models.get_upload_to),
        ),
    ]