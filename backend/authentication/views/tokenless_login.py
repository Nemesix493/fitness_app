from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import get_user_model, authenticate, login

from ..serializers.user import LoginUserSerializer


USER_MODEL = get_user_model()


class TokenlessLoginView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            serializer = LoginUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.authenticate_user(
                login=serializer.validated_data['login'],
                password=serializer.validated_data['password']
            )
            login(request, user)
            return Response({
                'success': True,
                'message': f'You are now authenticated as {user.username}!'
            })
        return Response(
            data={
                'message': f'You are already authenticated as {request.user.username}!'
                f'\n To reconnect, you need to log out first!'
            },
            status=400
        )

    def authenticate_user(self, login: str, password: str):
        user = authenticate(username=login, password=password)
        if user is not None:
            return user
        try:
            username = USER_MODEL.objects.get(email=login).username
            user = authenticate(username=username, password=password)
        except USER_MODEL.DoesNotExist:
            raise Http404('Error : login or password incorrect !')
        if user is not None:
            return user
        raise Http404('Error : login or password incorrect !')

