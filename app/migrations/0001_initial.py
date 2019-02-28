# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.TextField()),
                ('orientation', models.IntegerField()),
                ('position', models.IntegerField()),
                ('costume', models.IntegerField()),
                ('visibility', models.IntegerField()),
                ('size', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.TextField()),
                ('text', models.TextField()),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CSVs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('directory', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.TextField()),
                ('frelease', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.TextField()),
                ('blocks', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Duplicate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numduplicates', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fascinantes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('anidado', models.IntegerField()),
                ('colores', models.IntegerField()),
                ('geometricas', models.IntegerField()),
                ('artista', models.IntegerField()),
                ('points', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
                ('method', models.CharField(max_length=100)),
                ('time', models.DateField()),
                ('language', models.TextField(default=b'en')),
                ('score', models.IntegerField()),
                ('abstraction', models.IntegerField()),
                ('parallelization', models.IntegerField()),
                ('logic', models.IntegerField()),
                ('synchronization', models.IntegerField()),
                ('flowControl', models.IntegerField()),
                ('userInteractivity', models.IntegerField()),
                ('dataRepresentation', models.IntegerField()),
                ('spriteNaming', models.IntegerField()),
                ('initialization', models.IntegerField()),
                ('deadCode', models.IntegerField()),
                ('duplicateScript', models.IntegerField()),
                ('puntaje', models.IntegerField()),
                ('dialogos', models.IntegerField()),
                ('eventos', models.IntegerField()),
                ('puntuacion', models.IntegerField()),
                ('acciones', models.IntegerField()),
                ('mecanica', models.IntegerField()),
                ('objetivo', models.IntegerField()),
                ('anidado', models.IntegerField()),
                ('colores', models.IntegerField()),
                ('geometricas', models.IntegerField()),
                ('artista', models.IntegerField()),
                ('points', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mastery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abstraction', models.IntegerField()),
                ('paralel', models.IntegerField()),
                ('logic', models.IntegerField()),
                ('synchronization', models.IntegerField()),
                ('flowcontrol', models.IntegerField()),
                ('interactivity', models.IntegerField()),
                ('representation', models.IntegerField()),
                ('scoring', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('hashkey', models.TextField()),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='OrganizationHash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashkey', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('version', models.IntegerField()),
                ('score', models.IntegerField()),
                ('level', models.TextField()),
                ('path', models.TextField()),
                ('fupdate', models.TextField()),
                ('dashboard', models.ForeignKey(to='app.Dashboard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sprite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.TextField()),
                ('myproject', models.ForeignKey(to='app.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('daily_score', models.TextField()),
                ('basic', models.TextField(default=b'')),
                ('development', models.TextField(default=b'')),
                ('master', models.TextField(default=b'')),
                ('daily_projects', models.TextField(default=b'')),
                ('parallelism', models.IntegerField(default=0)),
                ('abstraction', models.IntegerField(default=0)),
                ('logic', models.IntegerField(default=0)),
                ('synchronization', models.IntegerField(default=0)),
                ('flowControl', models.IntegerField(default=0)),
                ('userInteractivity', models.IntegerField(default=0)),
                ('dataRepresentation', models.IntegerField(default=0)),
                ('deadCode', models.IntegerField(default=0)),
                ('duplicateScript', models.IntegerField(default=0)),
                ('spriteNaming', models.IntegerField(default=0)),
                ('initialization', models.IntegerField(default=0)),
                ('puntaje', models.IntegerField(default=0)),
                ('dialogos', models.IntegerField(default=0)),
                ('eventos', models.IntegerField(default=0)),
                ('puntuacion', models.IntegerField(default=0)),
                ('acciones', models.IntegerField(default=0)),
                ('mecanica', models.IntegerField(default=0)),
                ('objetivo', models.IntegerField(default=0)),
                ('anidado', models.IntegerField(default=0)),
                ('colores', models.IntegerField(default=0)),
                ('geometricas', models.IntegerField(default=0)),
                ('artista', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.TextField()),
                ('password', models.TextField()),
                ('email', models.TextField()),
                ('hashkey', models.TextField()),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='perceptivos',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mastery',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fascinantes',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='duplicate',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dead',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
    ]
