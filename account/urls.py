from django.urls import path

from account.views import CreateUserView, LoginView

urlpatterns = [
    path('accounts/', CreateUserView.as_view()),
    path('login/', LoginView.as_view())
]
