# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0007_remove_grumblr_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grumblr',
            name='user',
            field=models.OneToOneField(related_name='information', to=settings.AUTH_USER_MODEL),
        ),
    ]
