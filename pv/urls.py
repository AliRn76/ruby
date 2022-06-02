from django.urls import path
from pv.views import PVMessageAPIView, CreatePVAPIView

urlpatterns = [
    path('<int:user_id>/', CreatePVAPIView.as_view()),
    path('message/', PVMessageAPIView.as_view()),
]
