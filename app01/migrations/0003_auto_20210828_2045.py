# Generated by Django 3.1.7 on 2021-08-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_user_id_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='remark',
            field=models.TextField(default=1, verbose_name='备注'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='remark',
            field=models.TextField(default=123, verbose_name='备注'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vipproduct',
            name='remark',
            field=models.TextField(default=12, verbose_name='备注'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vipproductorder',
            name='remark',
            field=models.TextField(default=12, verbose_name='备注'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='courserecord',
            name='remark',
            field=models.TextField(default=123, verbose_name='备注'),
            preserve_default=False,
        ),
    ]
