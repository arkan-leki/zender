# Generated by Django 3.2.7 on 2021-09-28 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20210925_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldAcc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.DecimalField(decimal_places=2, max_digits=22, verbose_name='هاتوو')),
                ('loan', models.DecimalField(decimal_places=2, max_digits=22, verbose_name='دەرچووو')),
                ('date', models.DateField(auto_now_add=True, verbose_name='بەروار')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='رێکەوت')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oldacc_group', to='myapp.group', verbose_name='ناوی بنکە')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oldacc_compnay', to='myapp.localcompany', verbose_name='کڕیار')),
            ],
            options={
                'verbose_name_plural': 'هه\u200cژمار',
            },
        ),
    ]
