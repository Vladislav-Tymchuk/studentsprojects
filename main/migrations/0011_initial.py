# Generated by Django 4.0 on 2022-03-23 16:54

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0004_alter_customuser_avatar'),
        ('main', '0010_remove_group_groupteacher_remove_student_group_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupName', models.TextField(max_length=15)),
                ('groupYearAdmission', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.customuser')),
                ('teacherPatronymic', models.TextField(max_length=50)),
                ('teacherSubjects', models.TextField(max_length=511)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('authentication.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='groupTeacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.teacher'),
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement', models.FileField(upload_to='diplomas')),
                ('name', models.TextField(default='', max_length=127)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
            ],
        ),
    ]
