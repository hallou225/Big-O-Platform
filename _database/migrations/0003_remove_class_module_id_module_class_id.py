# Generated by Django 5.0.2 on 2024-03-16 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_database', '0002_language_module_term_year_remove_class_class_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='module_id',
        ),
        migrations.AddField(
            model_name='module',
            name='class_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='_database.class'),
        ),
    ]
