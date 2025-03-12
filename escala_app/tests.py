from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Medico, HorarioDisponivel

class FirebaseLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_without_token(self):
        """Testa login sem fornecer token do Firebase."""
        response = self.client.post("/api/auth/login/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_token(self):
        """Testa login com token inválido."""
        response = self.client.post("/api/auth/login/", {"idToken": "token_invalido"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


User = get_user_model()

class HorarioDisponivelTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='medico@example.com', 
            password='password123', 
            tipo='medico'
        )
        self.medico = Medico.objects.create(
            usuario=self.user,
            crm='12345',
            especialidade='Cardiologia',
            data_admissao='2023-01-01'
        )
        self.client.force_authenticate(user=self.user)

    def test_criar_horario_disponivel(self):
        """Testa criação de horário disponível por médico"""
        data = {
            'dia_semana': 'segunda',
            'hora_inicio': '08:00',
            'hora_fim': '12:00'
        }
        response = self.client.post('/api/horarios/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HorarioDisponivel.objects.count(), 1)

    def test_criar_horario_com_horario_invalido(self):
        """Testa criação de horário com hora início maior que hora fim"""
        data = {
            'dia_semana': 'segunda',
            'hora_inicio': '14:00',
            'hora_fim': '12:00'
        }
        response = self.client.post('/api/horarios/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Hora de início deve ser anterior à hora de fim.', response.data['non_field_errors'])

    def test_listar_horarios(self):
        """Testa listagem de horários disponíveis"""
        HorarioDisponivel.objects.create(
            medico=self.medico,
            dia_semana='segunda',
            hora_inicio='08:00',
            hora_fim='12:00'
        )
        response = self.client.get('/api/horarios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_excluir_horario(self):
        """Testa exclusão de horário disponível"""
        horario = HorarioDisponivel.objects.create(
            medico=self.medico,
            dia_semana='segunda',
            hora_inicio='08:00',
            hora_fim='12:00'
        )
        response = self.client.delete(f'/api/horarios/{horario.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HorarioDisponivel.objects.count(), 0)

    def test_usuario_nao_medico_tentando_criar_horario(self):
        """Testa se um paciente não pode criar horário disponível"""
        paciente = User.objects.create_user(
            email='paciente@example.com',
            password='password123',
            tipo='paciente'
        )
        self.client.force_authenticate(user=paciente)

        data = {
            'dia_semana': 'segunda',
            'hora_inicio': '08:00',
            'hora_fim': '12:00'
        }
        response = self.client.post('/api/horarios/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

