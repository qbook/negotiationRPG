# Generated by Django 4.2.5 on 2023-10-28 03:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameSetup', '0013_alter_gamesettings_round0end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesettings',
            name='round0End',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 28, 8, 59, 3, 541111, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round0Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 28, 4, 59, 3, 541062, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 4, 8, 59, 3, 541144, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round1Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 4, 3, 59, 3, 541118, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 11, 8, 59, 3, 541179, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round2Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 11, 3, 59, 3, 541152, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 18, 8, 59, 3, 541210, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round3Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 18, 3, 59, 3, 541186, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4End',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 8, 59, 3, 541340, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round4Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 3, 59, 3, 541216, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 8, 59, 3, 541377, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round5Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 3, 59, 3, 541347, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 8, 59, 3, 541404, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round6Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 3, 59, 3, 541383, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 8, 59, 3, 541431, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round7Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 3, 59, 3, 541410, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 23, 8, 59, 3, 541456, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round8Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 23, 3, 59, 3, 541436, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9End',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 8, 59, 3, 541482, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='round9Start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 3, 59, 3, 541461, tzinfo=datetime.timezone.utc)),
        ),
    ]