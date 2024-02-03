# Generated by Django 4.2.1 on 2024-02-03 13:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_customermessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermessage',
            name='full_name',
        ),
        migrations.AddField(
            model_name='customermessage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customermessage',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customermessage',
            name='mobile',
            field=models.CharField(max_length=20),
        ),
    ]
