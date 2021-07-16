from django.db import models
from django.urls import reverse
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm, widgets

# Create your models here.
class Medicos(models.Model):
    nome = models.CharField(verbose_name="Primeiro nome", max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_admissao = models.DateField(verbose_name="Data de admissão (DD/MM/AAAA)")
    status = models.BooleanField(default=True, verbose_name='Status(para desativar o médico desmarque esta opção):')

    def __str__(self):
        return "{} {}".format(self.nome, self.sobrenome)
    
    def get_absolute_url(self):
        return reverse("escala_app:detail",kwargs={'pk':self.pk})

class Postos(models.Model):
    nome = models.CharField(max_length=130)
    endereco = models.CharField(verbose_name="Endereço", max_length=250)
    status = models.BooleanField(default=True,verbose_name='Status(para desativar o posto desmarque esta opção):')

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("escala_app:postosdetail",kwargs={'pk':self.pk})

class Dia_de_Folga(models.Model):
    medico = models.ForeignKey(Medicos, related_name='dia_de_folga', limit_choices_to={'status': True}, on_delete=models.PROTECT)
    dia_folga = models.DateField(verbose_name="Dia de folga (DD/MM/AAAA)")

    def __str__(self):
        return str(self.dia_folga)
        
    def get_absolute_url(self):
        return reverse("escala_app:detail",kwargs={'pk':self.medico.pk})

class Escala(models.Model):
    data = models.DateField(verbose_name='Dia (DD/MM/AAAA)')
    posto = models.ForeignKey(Postos, related_name='escala_posto', limit_choices_to={'status': True}, on_delete=models.PROTECT)
    medico = models.ForeignKey(Medicos, related_name='escala_medico', limit_choices_to={'status': True}, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.data)
    
    def get_absolute_url(self):
        return reverse("escala_app:detail",kwargs={'pk':self.medico.pk})
