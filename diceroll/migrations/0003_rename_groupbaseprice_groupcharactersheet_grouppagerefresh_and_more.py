# Generated by Django 4.2.5 on 2023-10-24 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diceroll', '0002_alter_groupcharactersheet_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupcharactersheet',
            old_name='groupBasePrice',
            new_name='groupPageRefresh',
        ),
        migrations.RemoveField(
            model_name='groupcharactersheet',
            name='groupBaseUnits',
        ),
        migrations.AddField(
            model_name='groupcharactersheet',
            name='groupFirstRoll',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='groupcharactersheet',
            name='groupPlayNow',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
