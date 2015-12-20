# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0001_initial'),
        ('linapp', '0003_auto_20151127_0133'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sampling', '0003_auto_20151214_1536'),
    ]

    state_ops = [
        migrations.CreateModel(
            name='CellContentProtocol',
            fields=[
                ('protocol_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='linapp.Protocol')),
            ],
            bases=('linapp.protocol',),
        ),
        migrations.CreateModel(
            name='CellContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CellContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('comment', models.TextField()),
                ('cell', models.ForeignKey(to='sampling.Cell')),
                ('protocol', models.ForeignKey(blank=True, to='workflows.CellContentProtocol', null=True)),
                ('type', models.ForeignKey(to='workflows.CellContentType')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_ops,
        ),
        migrations.CreateModel(
            name='BarcodePair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('left', models.ForeignKey(to='parts.DNABarcode1')),
                ('right', models.ForeignKey(to='parts.DNABarcode2')),
            ],
        ),
        migrations.CreateModel(
            name='WorkFlowCell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barcodes', models.ForeignKey(to='workflows.BarcodePair')),
                ('content', models.ForeignKey(to='workflows.CellContent')),
            ],
        ),
    ]