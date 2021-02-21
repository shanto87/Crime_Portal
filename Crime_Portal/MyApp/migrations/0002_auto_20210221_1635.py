# Generated by Django 3.1.3 on 2021-02-21 10:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PSNamesDuplicate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('psname', models.CharField(max_length=150)),
            ],
        ),
        migrations.RenameField(
            model_name='generaldiary',
            old_name='verified',
            new_name='isVerified',
        ),
        migrations.RenameField(
            model_name='localintelligence',
            old_name='details',
            new_name='detail',
        ),
        migrations.RemoveField(
            model_name='generaldiarybyusers',
            name='creation_date_time',
        ),
        migrations.AddField(
            model_name='generaldiary',
            name='issuetime',
            field=models.TimeField(default=datetime.time(16, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generaldiarybyusers',
            name='creation_date',
            field=models.DateField(default=datetime.date(2001, 1, 1)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generaldiarybyusers',
            name='creation_time',
            field=models.TimeField(default=datetime.time(16, 0)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='localintelligence',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
