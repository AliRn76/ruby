from django.urls import path
from pv.views import PVMessageAPIView, CreatePVAPIView

urlpatterns = [
    path('<int:user_id>/', CreatePVAPIView.as_view()),
    path('message/', PVMessageAPIView.as_view(http_method_names=['post'])),
    path('message/<int:pv_id>/', PVMessageAPIView.as_view(http_method_names=['get'])),
]
