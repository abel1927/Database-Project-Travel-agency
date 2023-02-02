# Generated by Django 3.2 on 2021-05-22 02:35

import agencias.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_turist', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Agencia',
            fields=[
                ('IdA', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre')),
                ('direccion', models.CharField(max_length=100, verbose_name='Diercción')),
                ('noFax', models.CharField(max_length=32, verbose_name='Numero de Fax')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Excursion',
            fields=[
                ('IdE', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('lugarSalida', models.CharField(max_length=100, verbose_name='Lugar de Salida')),
                ('diaSalida', agencias.fields.DayWeekField(choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')], max_length=1, verbose_name='Dia de Salida')),
                ('horaSalida', models.TimeField(max_length=20, verbose_name='Hora de Salida')),
                ('lugarLlegada', models.CharField(max_length=100, verbose_name='Lugar de Llegada')),
                ('diaLlegada', agencias.fields.DayWeekField(choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miércoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')], max_length=1, verbose_name='Dia de Llegada')),
                ('horaLlegada', models.TimeField(max_length=20, verbose_name='Hora de Llegada')),
                ('precio', models.PositiveIntegerField(verbose_name='Precio')),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponible')),
            ],
        ),
        migrations.CreateModel(
            name='Facilidad',
            fields=[
                ('IdF', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('IdH', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('direccion', models.CharField(max_length=30)),
                ('categoria', models.PositiveIntegerField(verbose_name='Categoría')),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('CodigoP', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('duracion', models.PositiveIntegerField(verbose_name='Duración')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción')),
                ('precio', models.PositiveIntegerField(verbose_name='Precio')),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponible')),
                ('agencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.agencia', verbose_name='IdA')),
                ('facilidades', models.ManyToManyField(to='agencias.Facilidad')),
                ('hoteles', models.ManyToManyField(to='agencias.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Turista',
            fields=[
                ('IdT', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('pais', django_countries.fields.CountryField(max_length=50, verbose_name='Nacionalidad')),
                ('tipo', models.CharField(max_length=80)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReservacionPaquete',
            fields=[
                ('IdRP', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('companiaAereaRP', models.CharField(max_length=80, verbose_name='Compañía Aérea')),
                ('fecha', models.DateField(verbose_name='Fecha de Reservación')),
                ('cantidadParticipantes', models.PositiveIntegerField(verbose_name='Cantidad Participantes')),
                ('precioTotal', models.PositiveIntegerField(verbose_name='Precio')),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.paquete')),
                ('turista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.turista')),
            ],
        ),
        migrations.CreateModel(
            name='ReservacionIndividual',
            fields=[
                ('IdRI', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('companiaAerea', models.CharField(max_length=80, verbose_name='Compañía Aérea')),
                ('cantidadAcompansantes', models.PositiveIntegerField(verbose_name='Cantidad de Acompañantes')),
                ('precioTotal', models.PositiveIntegerField(verbose_name='Precio')),
                ('agencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.agencia')),
                ('excursiones', models.ManyToManyField(editable=False, to='agencias.Excursion')),
                ('turista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.turista')),
            ],
        ),
        migrations.CreateModel(
            name='ReservacionHotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IdH', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.hotel')),
                ('IdRI', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.reservacionindividual')),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('IdO', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripción')),
                ('precio', models.PositiveIntegerField(verbose_name='Precio')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerAgencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencias.agencia')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='excursion',
            name='hoteles',
            field=models.ManyToManyField(to='agencias.Hotel'),
        ),
        migrations.AddField(
            model_name='agencia',
            name='excursiones',
            field=models.ManyToManyField(to='agencias.Excursion'),
        ),
        migrations.AddField(
            model_name='agencia',
            name='hoteles',
            field=models.ManyToManyField(to='agencias.Hotel'),
        ),
    ]
