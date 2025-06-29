# Generated by Django 5.2.1 on 2025-06-09 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=128)),
                ('rol', models.CharField(choices=[('Admin', 'Administrador'), ('Empleado', 'Empleado'), ('Usuario', 'Usuario')], default='Usuario', max_length=15)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
