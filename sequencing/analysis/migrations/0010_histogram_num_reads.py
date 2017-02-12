# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-28 14:11
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import Sum
from django.template.defaultfilters import default


def update_histogram_num_reads(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    HistogramEntryReads = apps.get_model("analysis","HistogramEntryReads")
    Histogram = apps.get_model("analysis","Histogram")
    #run on each histogram
    for hist in Histogram.objects.using(db_alias).all():
        #sum up the values of num reads
        s = HistogramEntryReads.objects.using(db_alias).filter(histogram=hist).aggregate(Sum('num_reads')).popitem()[1]
        hist.num_reads = s
        hist.save()

trigger_creation = """create trigger histogram_entry_reads_trg after insert on analysis_histogramentryreads
                      for each row
                      begin
                        declare hist_id int(11);
                        declare inserted_val int(11);
                        declare curr_val int(11);
                        declare new_num_reads int(11);

                        set hist_id = NEW.histogram_id;
                        set inserted_val = new.num_reads;

                        select num_reads into curr_val from analysis_histogram where id = hist_id;
                        if curr_val is null THEN
                          set curr_val = 0;
                        END IF;

                        set new_num_reads = curr_val + inserted_val;

                        update analysis_histogram set num_reads = new_num_reads where id = hist_id;
                      end; """
class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0009_all_fmsv'),
    ]

    operations = [
        migrations.AddField(
            model_name='histogram',
            name='num_reads',
            field=models.PositiveIntegerField(null=True),
        ),

        migrations.RunPython(
            code=update_histogram_num_reads,
            reverse_code=migrations.RunPython.noop,
        ),

        migrations.RunSQL(
            sql = trigger_creation,
            reverse_sql= "drop trigger histogram_entry_reads_trg;",
        )

    ]