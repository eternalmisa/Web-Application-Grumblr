# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0019_auto_20151004_1339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinformation',
            old_name='follows',
            new_name='follow',
        ),
        migrations.AddField(
            model_name='userinformation',
            name='block',
            field=models.ManyToManyField(related_name='blocking', to=settings.AUTH_USER_MODEL),
        ),
    ]
