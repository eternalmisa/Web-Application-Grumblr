# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0033_auto_20151021_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dislike',
            name='user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='dislike',
        ),
        migrations.DeleteModel(
            name='Dislike',
        ),
    ]
