# Generated by Django 3.2 on 2022-06-27 18:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0007_auto_20220627_1738'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfeed',
            unique_together={('user', 'feed')},
        ),
    ]
