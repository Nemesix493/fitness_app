from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers import ManageUserSerializer


class ManageSelfUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            ManageUserSerializer(request.user).data
        )

    def put(self, request):
        serializer = ManageUserSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        serializer = ManageUserSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
