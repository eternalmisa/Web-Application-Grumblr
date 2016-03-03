# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20150922_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='grumblr',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 13, 26, 15, 672923, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
