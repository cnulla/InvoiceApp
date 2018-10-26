from django.urls import path
from accounts.views import (
    SignUpView,
    VerifyEmailView,
)

urlpatterns = [
        path('signup/', SignUpView.as_view(), name='signup'),
        path('verify-email', VerifyEmailView.as_view(), name='verify-email'),

]
