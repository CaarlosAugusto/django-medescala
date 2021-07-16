from django.contrib import admin
from escala_app.models import Medicos, Postos, Dia_de_Folga, Escala
# Register your models here.

admin.site.register(Medicos)
admin.site.register(Postos)
admin.site.register(Dia_de_Folga)
admin.site.register(Escala)