# Generated by Django 4.2.3 on 2023-09-17 02:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0003_cancel'),
    ]

    operations = [
        migrations.CreateModel(
            name='gifting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupDigit', models.IntegerField(blank=True, default=0, null=True)),
                ('groupClass', models.CharField(blank=True, max_length=200, null=True)),
                ('groupRPG', models.IntegerField(blank=True, default=0, null=True)),
                ('giftDateStamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('giftReceiver', models.IntegerField(blank=True, default=0, null=True)),
                ('giftAmount', models.IntegerField(blank=True, default=0, null=True)),
                ('giftSubject', models.TextField(blank=True, default='', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Flex Point Gift',
                'verbose_name_plural': 'Flex Point Gifts',
            },
        ),
        migrations.CreateModel(
            name='messaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupDigit', models.IntegerField(blank=True, default=0, null=True)),
                ('groupClass', models.CharField(blank=True, max_length=200, null=True)),
                ('groupRPG', models.IntegerField(blank=True, default=0, null=True)),
                ('messageDateStamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('messageReceiver', models.IntegerField(blank=True, default=0, null=True)),
                ('messageSubject', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('messageContent', models.TextField(blank=True, default='', null=True)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
