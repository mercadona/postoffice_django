from django.urls import path

from postoffice_django.api.views import ListMessagesView

urlpatterns = [
    path('messages/', ListMessagesView.as_view()),
]
