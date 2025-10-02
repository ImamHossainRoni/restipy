
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import AuthService
from .serializers import LoginSerializer, TokenSerializer
# Create your views here.


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    auth_service = AuthService()

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        email = serialized_data.validated_data['email']
        password = serialized_data.validated_data['password']

        user = self.auth_service.validate_user(email, password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = self.auth_service.get_tokens_for_user(user)
        return Response(TokenSerializer(tokens).data, status=status.HTTP_200_OK)
