# Generated by Django 3.2 on 2022-06-27 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_guide_feed_guid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfeed',
            name='url',
        ),
        migrations.AddField(
            model_name='feed',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
