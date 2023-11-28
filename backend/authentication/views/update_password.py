from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from ..serializers import UpdateUserPasswordSerializer


class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateUserPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response(
                data={
                    'message': 'Wrong old_password !'
                },
                status=403
            )
        try:
            validate_password(
                password=serializer.validated_data['new_password'],
                user=request.user
            )
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response(
                data={
                    'success': True,
                    'message': 'Password successfully updated!'
                }
            )
        except ValidationError as e:
            return Response(
                data={
                    'message': f'New password not valid!\n{e}'
                },
                status=400
            )
