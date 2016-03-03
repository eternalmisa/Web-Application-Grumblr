# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0010_auto_20151001_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformation',
            name='photoURL',
        ),
        migrations.AddField(
            model_name='userinformation',
            name='avatar',
            field=models.ImageField(default=b'/media/grumblr-avatar/default.jpg', upload_to=b'grumblr-avatar'),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='gender',
            field=models.CharField(default=b'', max_length=10),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='location',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='phoneNum',
            field=models.CharField(default=b'XXX-XXX-XXXX', max_length=50),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='school',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='short_bio',
            field=models.CharField(default=b'No instruction', max_length=420, blank=True),
        ),
    ]
