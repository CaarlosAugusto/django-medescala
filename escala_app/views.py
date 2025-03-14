from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import firebase_admin.auth as firebase_auth
from .models import HorarioDisponivel, Medico
from .serializers import *

User = get_user_model()

class FirebaseLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Verifica o token do Firebase e cria/autentica o usuário.
        """
        id_token = request.data.get("idToken")

        if not id_token:
            return Response({"error": "Token não fornecido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            email = decoded_token.get("email", "")
            nome = decoded_token.get("name", "").split(" ")[0]
            sobrenome = " ".join(decoded_token.get("name", "").split(" ")[1:])

            user, created = User.objects.get_or_create(
                email=email,
                defaults={"first_name": nome, "last_name": sobrenome, "tipo": 'medico',}
            )

            medico = Medico.objects.filter(usuario=user).first()
            primeiro_login = False if medico else True

            return Response({
                "message": "Usuário autenticado",
                "created": created,
                "user_id": user.id,
                "email": user.email,
                "tipo": user.tipo,
                "primeiro_login": primeiro_login
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class MedicoCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            if Medico.objects.filter(usuario=user).exists():
                return Response({"error": "Médico já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)

            data = request.data.copy()
            data['usuario'] = user.id

            serializer = MedicoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HorarioDisponivelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if not user.is_medico():
            return Response(
                {"error": "Somente médicos podem definir horários disponíveis"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            medico = Medico.objects.get(usuario=user)
        except Medico.DoesNotExist:
            return Response(
                {"error": "Médico não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Cria uma cópia mutável do request.data
        data = request.data.copy()

        if isinstance(data, list):
            for horario in data:
                horario['medico'] = medico.id

                # ✅ Verifica conflito de horário
                horario_existente = HorarioDisponivel.objects.filter(
                    medico=medico,
                    dia_semana=horario['dia_semana']
                ).exclude(
                    hora_inicio__gte=horario['hora_fim']
                ).exclude(
                    hora_fim__lte=horario['hora_inicio']
                ).first()

                if horario_existente:
                    return Response(
                        {
                            "error": "Conflito com horário existente.",
                            "horario_existente_id": horario_existente.id
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # ✅ Cria os horários após verificação
            serializer = HorarioDisponivelSerializer(data=data, many=True)
        else:
            data['medico'] = medico.id

            # ✅ Verifica conflito de horário para horário individual
            horario_existente = HorarioDisponivel.objects.filter(
                medico=medico,
                dia_semana=data['dia_semana']
            ).exclude(
                hora_inicio__gte=data['hora_fim']
            ).exclude(
                hora_fim__lte=data['hora_inicio']
            ).first()

            if horario_existente:
                return Response(
                    {
                        "error": "Conflito com horário existente.",
                        "horario_existente_id": horario_existente.id
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = HorarioDisponivelSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        
        if not user.is_medico():
            return Response({"error": "Somente médicos podem visualizar horários disponíveis"}, status=status.HTTP_403_FORBIDDEN)

        medico = Medico.objects.get(usuario=user)
        horarios = HorarioDisponivel.objects.filter(medico=medico)
        serializer = HorarioDisponivelSerializer(horarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = request.user

        if not user.is_medico():
            return Response({'error': 'Somente médicos podem excluir horários'}, status=status.HTTP_403_FORBIDDEN)

        try:
            horario = HorarioDisponivel.objects.get(id=pk, medico__usuario=user)
            horario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HorarioDisponivel.DoesNotExist:
            return Response({'error': 'Horário não encontrado'}, status=status.HTTP_404_NOT_FOUND)     
        
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return Response({"error": "Token não fornecido"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Captura e valida o token
            token = auth_header.split(' ')[1]
            decoded_token = firebase_auth.verify_id_token(token)

            email = decoded_token.get('email')
            if not email:
                return Response({"error": "Email não encontrado no token"}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.get(email=email)
            print(user)

            # Se o usuário for médico, retorna os dados de médico
            # if user.is_medico():
            #     medico = Medico.objects.get(usuario=user)
            #     serializer = MedicoSerializer(medico)
            #     return Response(serializer.data, status=status.HTTP_200_OK)

            # # Se o usuário for paciente, retorna os dados de paciente
            # elif user.is_paciente():
            #     paciente = Paciente.objects.get(usuario=user)
            #     serializer = PacienteSerializer(paciente)
            #     return Response(serializer.data, status=status.HTTP_200_OK)

            # # Se o usuário não for médico nem paciente, retorna os dados básicos
            # else:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Erro na autenticação: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)
    

# from django.http import request
# from django.shortcuts import render
# from django.urls import reverse_lazy
# from django.http import HttpResponseRedirect
# from escala_app.models import Medicos, Postos, Dia_de_Folga, Escala
# from escala_app.forms import MedicosForm, PostosForm, Dia_de_FolgaForm, EscalaForm
# from django.views.generic import (CreateView,UpdateView, 
#                                         ListView,DetailView,DeleteView)

# # Create your views here.
# def index(request):
#     return render(request, 'escala_app/index.html')

# class MedicosListView(ListView):
#     context_object_name = 'item_list'
#     extra_context={'name': 'Médicos'}
#     model = Medicos
#     template_name = 'escala_app/list.html'
#     def get_ordering(self):
#         ordering = self.request.GET.get('ordering', 'nome')
#         # validate ordering here
#         return ordering

# class MedicosDetailView(DetailView):
#     model = Medicos
#     context_object_name = 'medicos_detail'
#     template_name = 'escala_app/medicos_detail.html'
    
# class MedicosCreateView(CreateView):

#     def get(self, request, *args, **kwargs):
#         context = {'form': MedicosForm(), 'name': 'Médicos'}
#         return render(request, 'escala_app/form.html', context)

#     def post(self, request, *args, **kwargs):
#         form = MedicosForm(request.POST)
#         if form.is_valid():
#             medico = form.save()
#             medico.save()
#             return HttpResponseRedirect(reverse_lazy('escala_app:medicoslist'))
#         return render(request, 'escala_app/form.html', {'form': form})


# class MedicosUpdateView(UpdateView):
#     model = Medicos
#     fields = ['nome', 'sobrenome', 'data_admissao', 'status']
#     template_name = 'escala_app/form.html'

# class MedicosDeleteView(DeleteView):
#     model = Medicos
#     success_url = reverse_lazy("escala_app:medicos")

# class PostosCreateView(CreateView):

#     def get(self, request, *args, **kwargs):
#         context = {'form': PostosForm(), 'name': 'Postos'}
#         return render(request, 'escala_app/form.html', context)

#     def post(self, request, *args, **kwargs):
#         form = PostosForm(request.POST)
#         if form.is_valid():
#             posto = form.save()
#             posto.save()
#             return HttpResponseRedirect(reverse_lazy('escala_app:postoslist'))
#         return render(request, 'escala_app/form.html', {'form': form})

# class PostosListView(ListView):
#     model = Postos
#     extra_context={'name': 'Postos'}
#     context_object_name = 'item_list'
#     template_name = 'escala_app/list.html'

# class PostosDetailView(DetailView):
#     model = Postos
#     context_object_name = 'postos_detail'
#     template_name = 'escala_app/postos_detail.html'

# class PostosUpdateView(UpdateView):
#     model = Postos
#     fields = ['nome', 'endereco', 'status']
#     template_name = 'escala_app/form.html'


# class FolgaCreateView(CreateView):

#     def get(self, request, *args, **kwargs):
#         context = {'form': Dia_de_FolgaForm(), 'name': 'dias de folga'}
#         return render(request, 'escala_app/form.html', context)

#     def post(self, request, *args, **kwargs):
#         form = Dia_de_FolgaForm(request.POST)
#         if form.is_valid():
#             df = form.save()
#             df.save()
#             return HttpResponseRedirect(reverse_lazy('escala_app:folgalist'))
#         return render(request, 'escala_app/form.html', {'form': form})


# class FolgaListView(ListView):
#     model = Dia_de_Folga
#     extra_context={'name': 'dias de folga'}
#     context_object_name = 'item_list'
#     template_name = 'escala_app/list.html'
#     def get_ordering(self):
#         ordering = self.request.GET.get('ordering', 'dia_folga')
#         # validate ordering here
#         return ordering

# class FolgaUpdateView(UpdateView):
#     model = Dia_de_Folga
#     form_class = Dia_de_FolgaForm
#     template_name = 'escala_app/form.html'

# class FolgaDeleteView(DeleteView):
#     model = Dia_de_Folga
#     extra_context={'name': 'Folga'}
#     context_object_name = 'item'
#     success_url = reverse_lazy("escala_app:folgalist")

# class EscalaCreateView(CreateView):

#     def get(self, request, *args, **kwargs):
#         context = {'form': EscalaForm(), 'name': 'escala'}
#         return render(request, 'escala_app/form.html', context)

#     def post(self, request, *args, **kwargs):
#         form = EscalaForm(request.POST)
#         if form.is_valid():
#             escala = form.save()
#             escala.save()
#             return HttpResponseRedirect(reverse_lazy('escala_app:escalalist'))
#         return render(request, 'escala_app/form.html', {'form': form})

# class EscalaListView(ListView):
#     context_object_name = 'item_list'
#     extra_context={'name': 'Escala'}
#     model = Escala
#     template_name = 'escala_app/list.html'
#     def get_ordering(self):
#         ordering = self.request.GET.get('ordering', 'data')
#         # validate ordering here
#         return ordering

# class EscalaUpdateView(UpdateView):
#     model = Escala
#     form_class = EscalaForm
#     template_name = 'escala_app/form.html'

# class EscalaDeleteView(DeleteView):
#     model = Escala
#     template_name = 'escala_app/dia_de_folga_confirm_delete.html'
#     extra_context={'name': 'Escala'}
#     context_object_name = 'item'
#     success_url = reverse_lazy("escala_app:escalalist")