# Generated by Django 5.1.4 on 2025-01-02 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Church',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instID', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('church_type', models.CharField(max_length=255)),
                ('instName', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('instNote', models.CharField(max_length=255)),
                ('placeName', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('state_orig', models.CharField(max_length=255)),
                ('city_reg', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('attendingInstID', models.CharField(max_length=255)),
                ('memberType', models.CharField(max_length=255)),
                ('member', models.CharField(max_length=255)),
                ('affiliated', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('instID', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persID', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('persTitle', models.CharField(max_length=255)),
                ('persName', models.CharField(max_length=255)),
                ('persSuffix', models.CharField(max_length=255)),
                ('persNote', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('persID', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Small_Church',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instID', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('church_type', models.CharField(max_length=255)),
                ('instName', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('instNote', models.CharField(max_length=255)),
                ('placeName', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('state_orig', models.CharField(max_length=255)),
                ('city_reg', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('attendingInstID', models.CharField(max_length=255)),
                ('attendingChurch', models.CharField(max_length=255)),
                ('attendingChurchFrequency', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('instID', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Church_Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instID', models.CharField(max_length=255)),
                ('persID', models.CharField(max_length=255)),
                ('year_church', models.IntegerField()),
                ('year_person', models.IntegerField()),
                ('persTitle', models.CharField(max_length=255)),
                ('persName', models.CharField(max_length=255)),
                ('person_church', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='database.church')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_churches', to='database.person')),
            ],
            options={
                'unique_together': {('instID', 'persID', 'year_church', 'year_person')},
            },
        ),
        migrations.CreateModel(
            name='Church_Church',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instID', models.CharField(max_length=255)),
                ('attendingInstID', models.CharField(max_length=255)),
                ('year_church', models.IntegerField()),
                ('year_small_church', models.IntegerField()),
                ('church', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='small_churches', to='database.church')),
                ('small_church', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='churches', to='database.small_church')),
            ],
            options={
                'unique_together': {('instID', 'attendingInstID', 'year_church', 'year_small_church')},
            },
        ),
    ]
