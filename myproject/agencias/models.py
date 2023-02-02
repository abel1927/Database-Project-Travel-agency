from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from .fields import DayWeekField, FlyCompanyModelField
# Create your models here.


class User(AbstractUser):
    is_turist = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.username

class Turista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IdT = models.AutoField(unique=True,primary_key=True,null=False,auto_created=True,editable=False)
    nombre = models.CharField(verbose_name='Nombre',max_length = 50)
    pais = CountryField(verbose_name='Nacionalidad',max_length = 50)
    Tipo_turista_CHOICES = [
        ('I', 'Individual'),
        ('P', 'Paquete'),
        ('M', 'Mixto'),
    ]
    tipo = models.CharField(max_length=2,choices=Tipo_turista_CHOICES)
    def __str__(self):
        return self.nombre


class Hotel(models.Model):
    IdH = models.AutoField(primary_key=True,null=False,auto_created=True,editable=False)
    nombre = models.CharField(verbose_name='Nombre',max_length=30)
    direccion = models.CharField(max_length=30)
    categoria = models.PositiveIntegerField(verbose_name="Categoría",validators=[MinValueValidator(1),MaxValueValidator(5)])
    def __str__(self):
        return self.nombre

class Oferta(models.Model):
    IdO = models.AutoField(primary_key=True,null=False,auto_created=True,editable=False)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    descripcion = models.CharField('Descripción',max_length=100)
    precio = models.PositiveIntegerField('Precio')
    def __str__(self):
        return self.descripcion


class Excursion(models.Model):
    IdE = models.AutoField(primary_key=True,null=False,auto_created=True,editable=False)
    lugarSalida = models.CharField(verbose_name='Lugar de Salida', max_length=100)
    diaSalida = DayWeekField(verbose_name= 'Día de Salida')
    horaSalida = models.TimeField(verbose_name='Hora de Salida',max_length=20)
    lugarLlegada = models.CharField(verbose_name='Lugar de Llegada', max_length=100)
    diaLlegada = DayWeekField(verbose_name= 'Día de Llegada')
    horaLlegada = models.TimeField(verbose_name='Hora de Llegada',max_length=20)
    precio = models.PositiveIntegerField(verbose_name='Precio')
    hoteles = models.ManyToManyField(Hotel, blank=True)
    disponible = models.BooleanField(default=True, verbose_name = "Disponible")
    def __str__(self):
        return f'De {self.lugarSalida} a {self.lugarLlegada}'


class Agencia(models.Model):
    IdA = models.AutoField(verbose_name='IdA' ,serialize=True,primary_key=True,null=False,auto_created=True,editable=False)
    nombre = models.CharField(verbose_name='Nombre', max_length = 60)
    direccion = models.CharField(verbose_name='Diercción', max_length = 100)
    noFax = models.CharField(verbose_name='Numero de Fax',max_length = 32)
    email = models.EmailField()
    hoteles = models.ManyToManyField(Hotel, blank=True)
    excursiones = models.ManyToManyField(Excursion, blank=True)
    def __str__(self):
        return self.nombre


class ManagerAgencia(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Facilidad(models.Model):
    IdF = models.AutoField(primary_key=True,null=False,auto_created=True,editable=False)
    descripcion = models.CharField('Descripción',max_length=50)
    def __str__(self):
        return self.descripcion

class Paquete(models.Model):
    CodigoP = models.AutoField(primary_key=True,null=False,auto_created=True,editable=False)
    duracion = models.PositiveIntegerField(verbose_name='Duración')
    descripcion = models.CharField(verbose_name='Descripción',max_length=200)
    precio = models.PositiveIntegerField(verbose_name='Precio')
    agencia = models.ForeignKey(Agencia, verbose_name="Agencia", on_delete=models.CASCADE)
    hoteles = models.ManyToManyField(Hotel)
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    facilidades = models.ManyToManyField(Facilidad, blank=True)
    def __str__(self):
        return self.descripcion


class ReservacionPaquete(models.Model):
    IdRP = models.AutoField(primary_key=True,null=False,auto_created=True,editable=False)
    turista = models.ForeignKey(Turista,on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete,on_delete=models.CASCADE)
    companiaAerea = FlyCompanyModelField(verbose_name='Compañía Aérea')
    fecha = models.DateField('Fecha de Reservación')
    cantidadParticipantes = models.PositiveIntegerField('Cantidad Participantes')
    precioTotal = models.PositiveIntegerField('Precio')


class ReservacionIndividual(models.Model):
    IdRI = models.AutoField(primary_key=True,null=False,auto_created=True,editable=False)
    turista = models.ForeignKey(Turista,on_delete=models.CASCADE)
    agencia = models.ForeignKey(Agencia,on_delete=models.CASCADE)
    companiaAerea = FlyCompanyModelField(verbose_name='Compañía Aérea')
    cantidadAcompanhantes = models.PositiveIntegerField('Cantidad de Acompañantes')
    precioTotal = models.PositiveIntegerField('Precio')
    excursiones = models.ManyToManyField(Excursion, editable=False)
    hoteles = models.ManyToManyField(Hotel, editable=False, through='ReservacionHotel')


class ReservacionHotel(models.Model):
    reservacion = models.ForeignKey(ReservacionIndividual,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    fechaLlegada = models.DateField(verbose_name="Fecha Llegada")
    fechaSalida = models.DateField(verbose_name="Fecha Salida")


