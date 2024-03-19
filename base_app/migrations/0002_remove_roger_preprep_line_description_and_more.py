# Generated by Django 4.1 on 2024-03-17 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roger_preprep_line',
            name='description',
        ),
        migrations.AddField(
            model_name='roger_preprep_line',
            name='name',
            field=models.CharField(default='0', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roger_preprep_line',
            name='note',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='roger_preprep_line',
            name='line',
            field=models.TextField(max_length=200),
        ),
    ]
