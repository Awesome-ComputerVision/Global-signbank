# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-20 11:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0014_auto_20170913_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlendMorphology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='blendmorphology',
            name='glosses',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='glosses_comprising', to='dictionary.Gloss'),
        ),
        migrations.AddField(
            model_name='blendmorphology',
            name='parent_gloss',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blend_morphology', to='dictionary.Gloss'),
        ),
    ]