# Generated by Django 4.2.4 on 2025-06-28 08:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='excel_imports/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('records_imported', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('svg_id', models.CharField(help_text='ID of the region in SVG map', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StatisticsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('age_min', models.IntegerField()),
                ('age_max', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('jami', 'Jami'), ('erkak', 'Erkak'), ('ayol', 'Ayol')], max_length=10)),
                ('population', models.IntegerField()),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='dashboard_app.region')),
            ],
            options={
                'verbose_name': 'Statistics Data',
                'verbose_name_plural': 'Statistics Data',
                'indexes': [models.Index(fields=['region', 'year'], name='dashboard_a_region__c2d4f3_idx'), models.Index(fields=['age_min', 'age_max'], name='dashboard_a_age_min_deb6f4_idx'), models.Index(fields=['gender'], name='dashboard_a_gender_aa65de_idx')],
            },
        ),
    ]
