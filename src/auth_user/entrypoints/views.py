from typing import Optional

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from src.auth_user.adapters.repository import DjangoORMRepository
from src.auth_user.domain.auth import authentication
from src.auth_user.service_layer.serializers import RegistrationSerializer, AuthorizationSerializer, \
    ChangePasswordSerializer
from src.auth_user.service_layer.service import registration, authorization_, change_password


class BaseView(APIView):
    def get_login(self, request) -> Optional[str]:
        return authentication(request.headers)


class UserView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = registration(
            DjangoORMRepository(),
            serializer.validated_data["first_name"],
            serializer.validated_data["last_name"],
            serializer.validated_data["patronymic"],
            serializer.validated_data["email"],
            serializer.validated_data["login"],
            serializer.validated_data["password"]
        )
        return Response(response_data, status=HTTP_201_CREATED)


class AuthorizationView(APIView):
    def get(self, request):
        serializer = AuthorizationSerializer(data=request.headers)
        serializer.is_valid(raise_exception=True)
        token = authorization_(DjangoORMRepository(), serializer.validated_data["Authorization"])
        response = Response()
        response.set_cookie(key="refresh_token", value=token.pop("refresh_token"), httponly=True)
        return Response(data=token, status=HTTP_200_OK)


class ChangePassword(BaseView):
    def post(self, request):
        serializer_data = ChangePasswordSerializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        change_password(
            DjangoORMRepository(),
            self.get_login(request),
            serializer_data.validated_data["password"]
        )
        return Response(status=HTTP_201_CREATED)
