from django.shortcuts import get_object_or_404

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from blueprints.models import Blueprint
from keys.models import Key

from .serializers import BlueprintTestSerializer, BlueprintSerializer


class BlueprintTestViewSet(mixins.RetrieveModelMixin,
                           GenericViewSet):
    queryset = Blueprint.objects.all()
    serializer_class = BlueprintTestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, **kwargs):
        key = get_object_or_404(Key, pk=kwargs['pk'])
        queryset = Blueprint.objects.filter(key=key)
        serializer = BlueprintTestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlueprintViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = Blueprint.objects.all()
    serializer_class = BlueprintSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
