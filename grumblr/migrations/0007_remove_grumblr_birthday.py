# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0006_grumblr_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grumblr',
            name='birthday',
        ),
    ]
