from django.urls import path

from measurement.views import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListView

urlpatterns = [
    path('sensors/', CreateAPIView.as_view()),
    path('sensors/<pk>/', RetrieveUpdateAPIView.as_view()),
    path('sensors_list/', ListView.as_view()),
    path('measurements/', ListCreateAPIView.as_view()),
]
