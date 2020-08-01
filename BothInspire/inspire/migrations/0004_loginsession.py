# Generated by Django 3.0.5 on 2020-05-22 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0003_user_cp_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginSession',
            fields=[
                ('sessionid', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('sessiondata', models.TextField()),
                ('expire_time', models.DateTimeField()),
            ],
        ),
    ]