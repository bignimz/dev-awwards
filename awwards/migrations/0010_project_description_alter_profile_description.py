# Generated by Django 4.0.5 on 2022-06-13 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awwards', '0009_rename_date_project_posted_remove_project_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
