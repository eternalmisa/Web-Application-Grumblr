# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 21, 15, 14, 50, 430435, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
