# Generated by Django 4.2.16 on 2024-12-21 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app3', '0003_datosusuario_apellidousuario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datosusuario',
            name='apellidoUsuario',
        ),
        migrations.RemoveField(
            model_name='datosusuario',
            name='contraUsuario',
        ),
        migrations.RemoveField(
            model_name='datosusuario',
            name='emailUsuario',
        ),
        migrations.RemoveField(
            model_name='datosusuario',
            name='nombreUsuario',
        ),
        migrations.RemoveField(
            model_name='datosusuario',
            name='profesion',
        ),
        migrations.RemoveField(
            model_name='datosusuario',
            name='usernameUsuario',
        ),
    ]
