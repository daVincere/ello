# Generated by Django 2.1.12 on 2019-09-05 23:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190905_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='image',
            field=models.FileField(default=django.utils.timezone.now, upload_to='test/'),
            preserve_default=False,
        ),
    ]