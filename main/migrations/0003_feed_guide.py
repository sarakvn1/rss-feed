# Generated by Django 3.2 on 2022-06-27 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_source_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='guide',
            field=models.TextField(blank=True, null=True),
        ),
    ]
