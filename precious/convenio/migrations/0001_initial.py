# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 15:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArancelPractica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Observaciones')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Arancel de Práctica',
                'verbose_name_plural': 'Aranceles de Prácticas',
            },
        ),
        migrations.CreateModel(
            name='CodigoPractica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Observaciones')),
                ('codigo', models.CharField(max_length=10, verbose_name='Código de Práctica')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Código de Práctica',
                'ordering': ('codigo', 'prestador'),
                'verbose_name_plural': 'Códigos de Prácticas',
            },
        ),
        migrations.CreateModel(
            name='Convenio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio del convenio')),
            ],
            options={
                'verbose_name': 'Convenio con Prestador',
                'ordering': ('prestador',),
                'verbose_name_plural': 'Convenios con Prestadores',
            },
        ),
        migrations.CreateModel(
            name='DetalleArancel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arancel_homologado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arancel_homologado', to='convenio.ArancelPractica', verbose_name='Arancel Homologado')),
                ('arancel_prestador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arancel_prestador', to='convenio.ArancelPractica', verbose_name='Arancel del Prestador')),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenio.Convenio', verbose_name='Convenio')),
            ],
            options={
                'verbose_name': 'Detalle de Convenio de Aranceles de Práctica',
                'ordering': ('convenio', 'arancel_prestador'),
                'verbose_name_plural': 'Detalles de Convenio de Aranceles de Práctica',
            },
        ),
        migrations.CreateModel(
            name='DetalleCodigo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_homologado', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='codigo_homologado', to='convenio.CodigoPractica', verbose_name='Código Homologado')),
                ('codigo_prestador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='codigo_prestador', to='convenio.CodigoPractica', verbose_name='Código del Prestador')),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenio.Convenio', verbose_name='Convenio')),
            ],
            options={
                'verbose_name': 'Detalle de Convenio de Códigos de Práctica',
                'ordering': ('convenio', 'codigo_prestador'),
                'verbose_name_plural': 'Detalles de Convenio de Códigos de Práctica',
            },
        ),
        migrations.CreateModel(
            name='Prestador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre del Prestador')),
            ],
            options={
                'verbose_name': 'Prestador',
                'ordering': ('nombre',),
                'verbose_name_plural': 'Prestadores',
            },
        ),
        migrations.CreateModel(
            name='TipoPractica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tipo de Práctica')),
                ('prestador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenio.Prestador')),
            ],
            options={
                'verbose_name': 'Tipo de Práctica',
                'verbose_name_plural': 'Tipos de Prácticas',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prestador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenio.Prestador')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='convenio',
            name='prestador',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='convenio.Prestador', verbose_name='Prestador'),
        ),
        migrations.AddField(
            model_name='codigopractica',
            name='prestador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenio.Prestador'),
        ),
        migrations.AddField(
            model_name='codigopractica',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='convenio.TipoPractica', verbose_name='Tipo de Práctica'),
        ),
        migrations.AddField(
            model_name='arancelpractica',
            name='prestador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenio.Prestador'),
        ),
        migrations.AlterUniqueTogether(
            name='tipopractica',
            unique_together=set([('tipo', 'prestador')]),
        ),
        migrations.AlterUniqueTogether(
            name='codigopractica',
            unique_together=set([('tipo', 'codigo', 'prestador')]),
        ),
    ]
