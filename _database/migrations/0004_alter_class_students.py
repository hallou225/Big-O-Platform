# Generated by Django 5.0.2 on 2024-03-30 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_database', '0003_class_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to='_database.student'),
        ),
    ]
