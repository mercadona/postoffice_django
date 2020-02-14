from django.urls import path

from postoffice_django.api.views import DeleteMessageView, ListMessagesView

urlpatterns = [
    path('messages/', ListMessagesView.as_view()),
    path('messages/<int:pk>/', DeleteMessageView.as_view()),
]
