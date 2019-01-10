# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perceptivos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('puntaje', models.IntegerField()),
                ('dialogos', models.IntegerField()),
                ('eventos', models.IntegerField()),
                ('puntuacion', models.IntegerField()),
                ('acciones', models.IntegerField()),
                ('mecanica', models.IntegerField()),
                ('objetivo', models.IntegerField()),
                ('myproject', models.ForeignKey(to='app.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='stats',
            name='acciones',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stats',
            name='dialogos',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stats',
            name='eventos',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stats',
            name='mecanica',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stats',
            name='objetivo',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stats',
            name='puntaje',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stats',
            name='puntuacion',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
