# Generated by Django 4.0 on 2022-03-06 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to='avatars'),
        ),
    ]
