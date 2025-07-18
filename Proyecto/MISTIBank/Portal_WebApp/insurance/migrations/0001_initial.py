# Generated by Django 5.2.3 on 2025-06-19 03:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoSeguro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='SeguroContratado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_contratacion', models.DateField(auto_now_add=True)),
                ('tipo_seguro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.tiposeguro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('DEPOSITO', 'Depósito'), ('RETIRO', 'Retiro')], max_length=10)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.usuario')),
            ],
        ),
    ]
