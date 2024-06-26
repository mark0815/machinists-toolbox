# Generated by Django 4.0.3 on 2022-04-13 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Vendor',
                'verbose_name_plural': 'Vendors',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('flute_count', models.PositiveIntegerField()),
                ('flute_length', models.FloatField(verbose_name='Flute length (mm)')),
                ('overall_length', models.FloatField(verbose_name='Overall length (mm)')),
                ('diameter', models.FloatField(verbose_name='Diameter (mm)')),
                ('cutting_edge_angle', models.FloatField(default=90, verbose_name='Cutting edge angle KAPR (degree)')),
                ('material', models.CharField(choices=[('HSS', 'HSS'), ('CARBIDE', 'Carbide')], default='CARBIDE', max_length=10)),
                ('type', models.CharField(choices=[('ENDMILL', 'Endmill')], default='ENDMILL', max_length=10)),
                ('direction', models.CharField(choices=[('OFF', 'OFF'), ('CW', 'CW'), ('CCW', 'CCW')], default='CW', max_length=3)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tools', to='tool_library.vendor')),
            ],
            options={
                'ordering': ('vendor', 'diameter'),
            },
        ),
    ]
