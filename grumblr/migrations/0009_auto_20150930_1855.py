# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0008_auto_20150922_0943'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Grumblr',
            new_name='UserInformation',
        ),
    ]
