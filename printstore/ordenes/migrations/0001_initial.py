# Generated by Django 4.2.6 on 2023-12-09 03:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0005_alter_especificacion_tipo_valor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_ejemplares', models.IntegerField()),
                ('colores_impresion', models.CharField(choices=[('4+4', 'A colores en ambos lados'), ('4+1', 'A color al frente, reverson B/N'), ('4+0', 'A color al frente, nada al reverso'), ('1+1', 'A blanco y negro ambos lados'), ('1+0', 'A blanco y negro al frente, nada al reverso')], max_length=200)),
                ('ancho', models.DecimalField(decimal_places=2, max_digits=6)),
                ('largo', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('apellido_cliente', models.CharField(max_length=100)),
                ('dni_cliente', models.IntegerField()),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('fecha_entrega', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleOrdenProductoEspecificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_seleccionado', models.IntegerField()),
                ('fk_id_detalle_orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.detalleorden')),
                ('fk_id_producto_especificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.productoespecificacion')),
            ],
        ),
        migrations.AddField(
            model_name='detalleorden',
            name='fk_id_orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.orden'),
        ),
    ]