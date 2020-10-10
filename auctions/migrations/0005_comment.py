# Generated by Django 3.1 on 2020-10-09 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('time', models.CharField(max_length=64)),
                ('comment', models.TextField()),
                ('listingid', models.IntegerField()),
            ],
        ),
    ]