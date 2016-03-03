# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0029_auto_20151019_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 10, 20, 1, 15, 17, 592478, tzinfo=utc)),
        ),
    ]
