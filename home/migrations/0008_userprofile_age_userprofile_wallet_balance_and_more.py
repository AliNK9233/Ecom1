# Generated by Django 5.0 on 2024-01-02 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_userprofile_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wallet_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000016F98608040>', max_length=200),
        ),
    ]
