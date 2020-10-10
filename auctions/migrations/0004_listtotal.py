# Generated by Django 3.1 on 2020-10-09 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listtotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listingid', models.IntegerField()),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('link', models.CharField(blank=True, default=None, max_length=64, null=True)),
            ],
        ),
    ]
