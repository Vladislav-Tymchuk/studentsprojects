# Generated by Django 4.0 on 2022-03-12 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_customuser_avatar'),
        ('main', '0002_diploma_course_championship_certificate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement', models.ImageField(upload_to='diplomas')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
            ],
        ),
        migrations.RemoveField(
            model_name='championship',
            name='student',
        ),
        migrations.RemoveField(
            model_name='course',
            name='student',
        ),
        migrations.RemoveField(
            model_name='diploma',
            name='student',
        ),
        migrations.DeleteModel(
            name='Certificate',
        ),
        migrations.DeleteModel(
            name='Championship',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Diploma',
        ),
    ]
