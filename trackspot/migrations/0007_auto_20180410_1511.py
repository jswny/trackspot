# Generated by Django 2.0.2 on 2018-04-10 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackspot', '0006_auto_20180409_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='organization',
            field=models.CharField(blank=True, help_text='Enter a location for this user', max_length=50, null=True),
        ),
    ]
