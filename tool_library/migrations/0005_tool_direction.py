# Generated by Django 4.0.3 on 2022-04-04 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool_library', '0004_alter_tool_material_alter_tool_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='direction',
            field=models.CharField(choices=[('CW', 'CW'), ('CCW', 'CCW')], default='CW', max_length=3),
        ),
    ]
