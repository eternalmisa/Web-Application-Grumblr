# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0013_auto_20151004_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='avatar',
            field=models.ImageField(default=b'/static/grumblr/images/default.jpg', upload_to=b'grumblr-avatar'),
        ),
    ]
