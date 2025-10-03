from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import AuthService, UserReadService
from .serializers import LoginSerializer, TokenSerializer, UserSerializer


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


class UsersListAPIView(APIView):
    serializer_class = UserSerializer
    user_read_service = UserReadService()

    def get(self, request):
        users = self.user_read_service.get_all_users()
        serialized_data = self.serializer_class(users, many=True)
        return Response(serialized_data.data)

