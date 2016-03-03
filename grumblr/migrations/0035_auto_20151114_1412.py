# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0034_auto_20151023_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.ForeignKey(related_name='comments', to='grumblr.Message', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=30),
        ),
    ]
