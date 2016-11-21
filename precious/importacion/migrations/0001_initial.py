# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 12:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('convenio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorImportacionHomologacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje_error', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('tipo_practica', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('codigo_practica', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('nombre_practica', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('obs_practica', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('convenio', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('tipo_homologado', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('codigo_homologado', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('nombre_homologado', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('obs_homologado', models.CharField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrorImportacionPractica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje_error', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('tipo_practica', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('codigo_practica', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('nombre_practica', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('obs_practica', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('prestador', models.CharField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportarHomologacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='')),
                ('fila_titulo', models.BooleanField(default=True, verbose_name='La primer fila contiene los títulos de las columnas')),
                ('columna_tipo', models.IntegerField(default=0, help_text='Aunque sea una columna vacía la misma debe existir.', verbose_name="Columna de 'Tipo de Práctica'")),
                ('columna_codigo', models.IntegerField(default=1, verbose_name="Columna de 'Códigos de Prácticas'")),
                ('columna_nombre', models.IntegerField(default=2, verbose_name="Columna de 'Nombres de las Prácticas'")),
                ('columna_observaciones', models.IntegerField(blank=True, null=True, verbose_name="Columna de las 'Observaciones de las Prácticas'")),
                ('columna_tipo_homologado', models.IntegerField(verbose_name='Columna de Tipo de Práctica Homologada')),
                ('columna_codigo_homologado', models.IntegerField(verbose_name='Columna de Código de Práctica Homologada')),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenio.Convenio')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ImportarHomologacion_creador', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ImportarHomologacion_modificador', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Importar Homologación en formato Excel (.xls)',
                'verbose_name_plural': 'Importar Homologación en formato Excel (.xls)',
            },
        ),
        migrations.CreateModel(
            name='ImportarPracticas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='')),
                ('fila_titulo', models.BooleanField(default=True, verbose_name='La primer fila contiene los títulos de las columnas')),
                ('columna_tipo', models.IntegerField(default=0, help_text='Aunque sea una columna vacía la misma debe existir.', verbose_name="Columna de 'Tipo de Práctica'")),
                ('columna_codigo', models.IntegerField(default=1, verbose_name="Columna de 'Códigos de Prácticas'")),
                ('columna_nombre', models.IntegerField(default=2, verbose_name="Columna de 'Nombres de las Prácticas'")),
                ('columna_observaciones', models.IntegerField(blank=True, null=True, verbose_name="Columna de las 'Observaciones de las Prácticas'")),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ImportarPracticas_creador', to=settings.AUTH_USER_MODEL)),
                ('prestador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenio.Prestador')),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ImportarPracticas_modificador', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Importar Prácticas en formato Excel (.xls)',
                'verbose_name_plural': 'Importar Prácticas en formato Excel (.xls)',
            },
        ),
    ]
