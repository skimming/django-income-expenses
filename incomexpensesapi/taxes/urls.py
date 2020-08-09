from django.urls import path
from . import views
from django.urls import path, include
from .views import TaxDetailAPIView, TaxListAPIView

urlpatterns = [
    path('', views.TaxListAPIView.as_view(), name='taxes'),
    path('<int:id>', views.TaxDetailAPIView.as_view(), name='tax')
]