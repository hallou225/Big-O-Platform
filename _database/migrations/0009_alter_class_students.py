# Generated by Django 5.0.2 on 2024-03-30 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_database', '0008_alter_class_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(related_name='student_class', to='_database.student'),
        ),
    ]