from rest_framework import serializers
from .models import *

class HorarioDisponivelSerializer(serializers.ModelSerializer):
    medico = serializers.PrimaryKeyRelatedField(queryset=Medico.objects.all())

    class Meta:
        model = HorarioDisponivel
        fields = '__all__'
        read_only_fields = ['medico']

    def validate(self, data):
        if data['hora_inicio'] >= data['hora_fim']:
            raise serializers.ValidationError("Hora de início deve ser anterior à hora de fim.")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'tipo', 'telefone']

class MedicoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Medico
        fields = ['usuario', 'crm', 'especialidade', 'data_admissao', 'status']

class PacienteSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Paciente
        fields = ['usuario', 'data_nascimento', 'endereco']
