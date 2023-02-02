from django.db import models

# Create your models here.

class SolicitudAsociacionAgencia(models.Model):
    IdS = models.AutoField(primary_key=True, editable=False, null=False, auto_created=True)
    nombre = models.CharField(name="Nombre de la agencia", max_length=50)
    direccion = models.CharField(name='Direccón principal', max_length=120)
    email_agencia = models.EmailField(name= 'email agencia')
    noFax = models.CharField(name="Fax", max_length=20)
    entidad_bancaria = models.CharField(name="Entidad bancaria de respaldo", max_length=80)
    anhos_activa = models.PositiveIntegerField(name="Años de antigüedad")
    manager_nombre = models.CharField(name="Manager nombre", max_length=70)
    manager_email = models.EmailField(name= 'email manager')
    tiempo_con_hv = models.PositiveIntegerField(verbose_name="Cuánto tiempo espera trabajar con nosotros?",
                name='Pespectiva')
    

