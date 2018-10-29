from django.urls import path
from accounts.views import (
    SignUpView,
    VerifyEmailView,
    VerifyTokenView,
)

urlpatterns = [
        path('signup/', SignUpView.as_view(), name='signup'),
        path('verify-email', VerifyEmailView.as_view(), name='verify-email'),
        path('verify-token/<str:token>/', VerifyTokenView.as_view(), name='verify-token'),

]
