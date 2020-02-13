from django.urls import path

from postoffice_django.api.views import MessagesView

urlpatterns = [
    path('messages/', MessagesView.as_view()),
]
