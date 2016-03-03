# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0024_userinformation_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='posted_message',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='writer',
        ),
        migrations.RemoveField(
            model_name='message',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='message',
            name='like',
        ),
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 20, 33, 49, 408142, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
