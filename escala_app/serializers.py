from rest_framework import serializers
from .models import HorarioDisponivel

class HorarioDisponivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioDisponivel
        fields = '__all__'
        read_only_fields = ['medico']

    def validate(self, data):
        if data['hora_inicio'] >= data['hora_fim']:
            raise serializers.ValidationError("Hora de início deve ser anterior à hora de fim.")
        return data
