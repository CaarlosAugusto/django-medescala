from firebase_admin import auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        # Verifica se o token começa com 'Bearer'
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Token inválido')

        token = auth_header.split(' ')[1]

        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')

            email = decoded_token.get('email')
            if not email:
                raise AuthenticationFailed('Email não fornecido no token')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": decoded_token.get("name", "").split(" ")[0],
                    "last_name": " ".join(decoded_token.get("name", "").split(" ")[1:]),
                    "tipo": "medico"  # Define tipo padrão como médico (se precisar mudar, ajuste aqui)
                }
            )
            return (user, None)
        except Exception as e:
            raise AuthenticationFailed(f'Erro na autenticação: {str(e)}')

