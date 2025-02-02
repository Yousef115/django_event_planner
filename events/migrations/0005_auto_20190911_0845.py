# Generated by Django 2.2.5 on 2019-09-11 05:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_auto_20190908_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.PositiveSmallIntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='events.Event')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
