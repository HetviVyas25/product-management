# Generated by Django 4.1.1 on 2023-04-07 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_addr2_address_addr1'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='addr2',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]