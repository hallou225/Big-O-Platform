# Generated by Django 5.0.2 on 2024-04-19 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_database', '0019_merge_0017_merge_20240412_1444_0018_delete_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAlgorithm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.TextField(max_length=2000, null=True)),
                ('score', models.CharField(max_length=20, null=True)),
                ('percentage', models.CharField(max_length=20, null=True)),
                ('algorithm_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='_database.algorithm')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='_database.student')),
            ],
        ),
    ]
