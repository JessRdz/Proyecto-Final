# Generated by Django 2.2.1 on 2019-05-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(help_text='Fecha de registro', max_length=40)),
                ('servicio', models.CharField(help_text='Servicio', max_length=20)),
                ('size', models.IntegerField(help_text='Tamaño en bytes del flujo', max_length=10)),
                ('ip_origen', models.CharField(help_text='IP del dispositivo origen', max_length=20)),
                ('ip_destino', models.CharField(help_text='IP del dispositivo destino', max_length=20)),
            ],
        ),
    ]