# Generated by Django 4.2.17 on 2025-01-29 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_church_diocese_small_church_diocese'),
    ]

    operations = [
        migrations.CreateModel(
            name='Small_Church_Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instID', models.CharField(max_length=255)),
                ('persID', models.CharField(max_length=255)),
                ('year_church', models.IntegerField()),
                ('year_person', models.IntegerField()),
                ('persTitle', models.CharField(max_length=255)),
                ('persName', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_small_churches', to='database.person')),
                ('person_church', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='small_church_persons', to='database.small_church')),
            ],
            options={
                'unique_together': {('instID', 'persID', 'year_church', 'year_person')},
            },
        ),
    ]
