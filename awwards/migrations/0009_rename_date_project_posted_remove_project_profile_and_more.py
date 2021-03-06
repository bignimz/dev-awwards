# Generated by Django 4.0.5 on 2022-06-12 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('awwards', '0008_remove_project_user_remove_project_profile_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='date',
            new_name='posted',
        ),
        migrations.RemoveField(
            model_name='project',
            name='profile',
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
