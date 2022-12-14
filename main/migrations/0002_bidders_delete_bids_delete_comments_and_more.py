# Generated by Django 4.1 on 2022-12-13 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bidders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='bids',
        ),
        migrations.DeleteModel(
            name='comments',
        ),
        migrations.RemoveField(
            model_name='winner',
            name='bid_win_list',
        ),
        migrations.RemoveField(
            model_name='auctionlist',
            name='category',
        ),
        migrations.RemoveField(
            model_name='auctionlist',
            name='desc',
        ),
        migrations.AddField(
            model_name='auctionlist',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='auctionlist',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auctionlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='watchlist',
        ),
        migrations.DeleteModel(
            name='winner',
        ),
        migrations.AddField(
            model_name='bidders',
            name='list_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.auctionlist'),
        ),
        migrations.AddField(
            model_name='bidders',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
