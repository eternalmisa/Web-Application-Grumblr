# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_grumblr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grumblr',
            name='phoneNum',
            field=models.CharField(max_length=20),
        ),
    ]
