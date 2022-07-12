from django.urls import path
from pv.views import PVMessageAPIView, CreatePVAPIView, ReadPVMessageAPIView, UpdateDestroyPVMessageAPIView

urlpatterns = [
    path('<int:user_id>/', CreatePVAPIView.as_view()),
    path('message/', PVMessageAPIView.as_view(http_method_names=['post'])),
    path('message/<int:pv_id>/', PVMessageAPIView.as_view(http_method_names=['get'])),
    path('message/<int:pv_id>/<int:pv_message_id>/', UpdateDestroyPVMessageAPIView.as_view(http_method_names=['patch', 'delete'])),
    path('message/<int:pv_id>/<int:pv_message_id>/read/', ReadPVMessageAPIView.as_view()),
]
