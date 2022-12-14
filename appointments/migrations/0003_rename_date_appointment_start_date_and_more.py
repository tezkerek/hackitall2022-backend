# Generated by Django 4.1.4 on 2022-12-10 22:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_alter_appointment_branch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='date',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='duration',
        ),
        migrations.AddField(
            model_name='appointment',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
