# Generated by Django 3.2.18 on 2023-05-17 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asn', '0009_alter_asnlistmodel_transportation_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asnlistmodel',
            name='transportation_fee',
            field=models.JSONField(default=dict, verbose_name='Transportation Fee'),
        ),
    ]
