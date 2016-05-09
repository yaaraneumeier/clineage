# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-09 19:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('amplicons', '0002_create_ter_amplicons'),
        ('planning', '0004_auto_20160420_1500'),
        ('workflows', '0004_auto_20160420_1501'),
        ('runs', '0002_auto_20160420_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdamAmpliconReads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_offset', models.IntegerField(null=True)),
                ('fastq1', models.FilePathField()),
                ('fastq2', models.FilePathField()),
                ('fastqm', models.FilePathField()),
                ('amplicon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amplicons.Amplicon')),
            ],
        ),
        migrations.CreateModel(
            name='AdamMarginAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_sam', models.FilePathField()),
            ],
        ),
        migrations.CreateModel(
            name='AdamMergedReads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembled_fastq', models.FilePathField()),
                ('discarded_fastq', models.FilePathField()),
                ('unassembled_forward_fastq', models.FilePathField()),
                ('unassembled_reverse_fastq', models.FilePathField()),
            ],
        ),
        migrations.CreateModel(
            name='AdamMSVariations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_dump_dir', models.FilePathField(allow_files=False, allow_folders=True)),
                ('padding', models.PositiveIntegerField()),
                ('microsatellites_version', models.IntegerField()),
                ('amplicon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amplicons.Amplicon')),
            ],
        ),
        migrations.CreateModel(
            name='AdamReadsIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_dump_dir', models.FilePathField(allow_files=False, allow_folders=True)),
                ('included_reads', models.CharField(choices=[('M', 'Only merged'), ('F', 'Merged and unassembled_forward')], max_length=1)),
                ('padding', models.IntegerField(default=5)),
                ('merged_reads', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.AdamMergedReads')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Histogram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='HistogramEntryReads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microsatellites_version', models.IntegerField()),
                ('num_reads', models.PositiveIntegerField()),
                ('fastq1', models.FilePathField()),
                ('fastq2', models.FilePathField()),
                ('fastqm', models.FilePathField(null=True)),
                ('amplicon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amplicons.Amplicon')),
            ],
        ),
        migrations.CreateModel(
            name='MicrosatelliteHistogramGenotype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repeat_number', models.PositiveIntegerField()),
                ('microsatellite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planning.Microsatellite')),
            ],
        ),
        migrations.CreateModel(
            name='SampleReads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fastq1', models.FilePathField()),
                ('fastq2', models.FilePathField()),
                ('barcoded_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflows.BarcodedContent')),
                ('demux', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='runs.Demultiplexing')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflows.Library')),
            ],
        ),
        migrations.CreateModel(
            name='SNPHistogramGenotype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=1)),
                ('snp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planning.SNP')),
            ],
        ),
        migrations.CreateModel(
            name='AdamHistogram',
            fields=[
                ('histogram_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='analysis.Histogram')),
                ('assignment_sam', models.FilePathField()),
            ],
            bases=('analysis.histogram',),
        ),
        migrations.AddField(
            model_name='histogramentryreads',
            name='histogram',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.Histogram'),
        ),
        migrations.AddField(
            model_name='histogramentryreads',
            name='microsatellite_genotypes',
            field=models.ManyToManyField(to='analysis.MicrosatelliteHistogramGenotype'),
        ),
        migrations.AddField(
            model_name='histogramentryreads',
            name='snp_genotypes',
            field=models.ManyToManyField(to='analysis.SNPHistogramGenotype'),
        ),
        migrations.AddField(
            model_name='histogram',
            name='sample_reads',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.SampleReads'),
        ),
        migrations.AddField(
            model_name='adammergedreads',
            name='sample_reads',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.SampleReads'),
        ),
        migrations.AddField(
            model_name='adammarginassignment',
            name='reads_index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.AdamReadsIndex'),
        ),
        migrations.AddField(
            model_name='adamampliconreads',
            name='margin_assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.AdamMarginAssignment'),
        ),
        migrations.AlterIndexTogether(
            name='histogramentryreads',
            index_together=set([('histogram', 'amplicon', 'microsatellites_version')]),
        ),
        migrations.AlterIndexTogether(
            name='adammsvariations',
            index_together=set([('amplicon', 'padding', 'microsatellites_version')]),
        ),
        migrations.AddField(
            model_name='adamhistogram',
            name='amplicon_reads',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.AdamAmpliconReads'),
        ),
        migrations.AddField(
            model_name='adamhistogram',
            name='ms_variations',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.AdamMSVariations'),
        ),
        migrations.AlterIndexTogether(
            name='adamampliconreads',
            index_together=set([('margin_assignment', 'amplicon')]),
        ),
    ]
