# Generated by Django 3.0.5 on 2020-05-08 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('group', models.CharField(max_length=36)),
                ('file', models.FileField(default='files/default.jpg', upload_to='files/')),
            ],
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('img', models.FileField(default='files/gift.jpg', upload_to='files/')),
                ('title', models.CharField(max_length=50)),
                ('sweet', models.IntegerField()),
                ('created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=100)),
                ('sex', models.BooleanField()),
                ('sweet', models.IntegerField()),
                ('head_img', models.FileField(default='files/head_img.jpg', upload_to='files/')),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('reason', models.TextField()),
                ('sweet', models.IntegerField()),
                ('approval_status', models.IntegerField()),
                ('file_group', models.CharField(max_length=36)),
                ('created', models.DateTimeField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_applicant', to='inspire.User')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviewer', to='inspire.User')),
            ],
        ),
    ]