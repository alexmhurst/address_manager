# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-03 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addman', '0006_auto_20160302_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='status',
            field=models.CharField(choices=[(b'UNPARSED', b'Not yet processed'), (b'FAILED', b'No match found'), (b'WARN', b'Tentative match, may be undeliverable'), (b'CONFIRMABLE', b'Tentative match, confirmation required'), (b'VALIDATED', b'Validated and deliverable')], default=b'UNPARSED', max_length=50),
        ),
    ]
