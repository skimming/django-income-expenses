from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.
from .serializers import TaxSerializer
from .models import Tax
from rest_framework import permissions
from .permissions import IsOwner


class TaxListAPIView(ListCreateAPIView) :
    serializer_class = TaxSerializer
    queryset = Tax.objects.all()
    # identifies permissions required
    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TaxDetailAPIView(RetrieveUpdateDestroyAPIView) :
    serializer_class=TaxSerializer
    queryset = Tax.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
