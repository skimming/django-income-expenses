from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.
from .serializers import ExpenseSerializer
from .models import Expense
from rest_framework import permissions
from .permissions import IsOwner


class ExpenseListAPIView(ListCreateAPIView) :  # ListCreateAPIView will provide a list return and a post single
    serializer_class=ExpenseSerializer
    queryset = Expense.objects.all()
    # identifies permissions required
    permission_classes = (permissions.IsAuthenticated,)  # need to override with permissions


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)  # when create is requested, will save with current user info as owner

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)  # when querylist is requested (get) will only return those that he created



class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView) :  # RetrieveUpdateDestroyAPIView will automatically create get/put/patch/delete APIs based on ID
    serializer_class=ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
