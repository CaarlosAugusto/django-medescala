# from django import forms
# from django.core.exceptions import ValidationError
# from escala_app.models import Medicos, Postos, Dia_de_Folga, Escala

# class MedicosForm(forms.ModelForm):
#     data_admissao = forms.DateField(input_formats=['%d/%m/%Y', ])
#     class Meta:
#         model = Medicos
#         fields = ('nome', 'sobrenome', 'data_admissao')

# class PostosForm(forms.ModelForm):
#     class Meta:
#         model = Postos
#         fields = ('nome', 'endereco')

# class Dia_de_FolgaForm(forms.ModelForm):
#     dia_folga = forms.DateField(input_formats=['%d/%m/%Y', ])
#     class Meta:
#         model = Dia_de_Folga
#         fields = ('medico', 'dia_folga')

#     def clean(self):
#         cleaned_data = super().clean()
#         data = cleaned_data.get("dia_folga")
#         medico = cleaned_data.get("medico")
#         folga_teste = Escala.objects.filter(data=data)
#         #
        
#         dp_teste = Medicos.objects.filter(dia_de_folga__dia_folga__contains=data)
        
#         if dp_teste:
#             query = [item for item in dp_teste]
#             if medico in query:
#                 # Only do something if both fields are valid so far.
#                 raise ValidationError(
#                     "Este médico já está com folga marcada para este dia!"
#                 )

#         if folga_teste:
#             query = [item for item in folga_teste]
#             for each in query:
#                 if medico == each.medico:
#                     # Only do something if both fields are valid so far.
#                     raise ValidationError(
#                         "Este médico já está escalado neste dia!\nPara inserir folga nesse dia remova-o da escala."
#                     )

# class EscalaForm(forms.ModelForm):
#     data = forms.DateField(input_formats=['%d/%m/%Y', ])
#     class Meta:
#         model = Escala
#         fields = ('medico', 'data', 'posto')

#     def clean(self):
#         cleaned_data = super().clean()
#         data = cleaned_data.get("data")
#         medico = cleaned_data.get("medico")
#         posto = cleaned_data.get("posto")
#         folga_teste = Medicos.objects.filter(dia_de_folga__dia_folga__contains=data)
#         dp_medico = Escala.objects.filter(data=data)
        
#         if folga_teste:
#             query = [item for item in folga_teste]
#             if medico in query:
#                 # Only do something if both fields are valid so far.
#                 raise ValidationError(
#                     "Este médico estará de folga nesse dia!"
#                 )
#         if dp_medico:
#             query = [item for item in dp_medico]
#             for each in query:
#                 if medico == each.medico:
#                     # Only do something if both fields are valid so far.
#                     raise ValidationError(
#                         "Este médico já esta escalado para este dia!"
#                     )
#                 elif posto == each.posto:
#                     raise ValidationError(
#                         "Este posto já está ocupado para este dia!"
#                     )