from django.urls import path

from questions import views

urlpatterns = [
    path("assistant/", views.AssistantAPIView.as_view())
]
