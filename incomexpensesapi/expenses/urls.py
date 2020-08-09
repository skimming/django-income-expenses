from django.urls import path
from . import views
from django.urls import path, include
from .views import ExpenseDetailAPIView, ExpenseListAPIView

urlpatterns = [
    path('', views.ExpenseListAPIView.as_view(), name='expenses'),
    path('<int:id>', views.ExpenseDetailAPIView.as_view(), name='expense')
]