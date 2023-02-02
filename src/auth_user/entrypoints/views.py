from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from src.auth_user.adapters.repository import DjangoORMRepository
from src.auth_user.service_layer.serializers import RegistrationSerializer, AuthorizationSerializer
from src.auth_user.service_layer.service import registration, authorization


class UserView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = registration(
            DjangoORMRepository(),
            serializer.validated_data['first_name'],
            serializer.validated_data['last_name'],
            serializer.validated_data['patronymic'],
            serializer.validated_data['email'],
            serializer.validated_data['login'],
            serializer.validated_data['password']
        )
        return Response(response_data, status=HTTP_201_CREATED)


class SecurityToken(APIView):
    def get(self, request):
        serializer = AuthorizationSerializer(data=request.headers)
        serializer.is_valid(raise_exception=True)
        token = authorization(DjangoORMRepository(), serializer.validated_data["Authorization"])
        response = Response()
        response.set_cookie(key="refresh_token", value=token.pop("refresh_token"), httponly=True)
        return Response(data=token, status=HTTP_200_OK)
