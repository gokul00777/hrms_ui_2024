# Generated by Django 4.2 on 2023-09-11 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_management_app', '0003_alter_documents_passport'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
