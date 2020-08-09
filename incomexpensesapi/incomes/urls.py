from django.urls import path
from . import views
from django.urls import path, include
from .views import IncomeDetailAPIView, IncomeListAPIView

urlpatterns = [
    path('', views.IncomeListAPIView.as_view(), name='incomes'),
    path('<int:id>', views.IncomeDetailAPIView.as_view(), name='income')
]