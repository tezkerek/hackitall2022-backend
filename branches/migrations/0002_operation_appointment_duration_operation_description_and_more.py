# Generated by Django 4.1.4 on 2022-12-10 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='appointment_duration',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operation',
            name='description',
            field=models.CharField(default='test', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='branch',
            name='break_schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='break_schedule', to='branches.schedule'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='mf_schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='mf_schedule', to='branches.schedule'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='satsun_schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='satsun_schedule', to='branches.schedule'),
        ),
    ]
