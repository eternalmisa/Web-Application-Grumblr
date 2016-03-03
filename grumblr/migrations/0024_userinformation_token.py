# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0023_auto_20151005_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='token',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
