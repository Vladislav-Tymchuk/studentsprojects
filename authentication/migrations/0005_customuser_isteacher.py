# Generated by Django 4.0 on 2022-03-24 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='isTeacher',
            field=models.BooleanField(default=False),
        ),
    ]
