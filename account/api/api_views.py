
from django.contrib.auth import authenticate, logout
from django.conf import settings as app_settings

from .serializers import UserLoginSerializer, UserSerializer, EducatorsSerializer

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from .renderer import CustomRenderer
from django.contrib.auth import get_user_model
User = get_user_model()
STATUS = app_settings.STATUS_CODES


class LoginAPIView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            print(serializer.is_valid())
            if serializer.is_valid():
                return Response({
                    "success": True,
                    'status': STATUS.get('success', ''),
                    "token": serializer.validated_data,
                    "detail": "Login success"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "success": False,
                'status': STATUS.get('error', ''),
                # "token": serializer.errors,
                "detail":  "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (CustomRenderer,)


class EducatorsOnly(generics.ListAPIView):
    serializer_class = EducatorsSerializer
    renderer_classes = (CustomRenderer, )

    def get_queryset(self):
        return User.objects.filter(role='teacher')


    # def post(self, request):
    #     serializer = UserSerializer(request.data)
    #     print(serializer)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutAPIView(APIView):
#
#     def get(self, request):
#         request = request.user.auth_token.delete()
#         logout(request)
#         return Response('You logged out successfully')
