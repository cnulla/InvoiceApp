from django.urls import path
from accounts.views import (
    SignUpView,
    VerifyEmailView,
    VerifyTokenView,
    SignInView,
    SignOutView,
)

urlpatterns = [
        path('signup/', SignUpView.as_view(), name='signup'),
        path('signin/', SignInView.as_view(), name='signin'),
        path('signout/', SignOutView.as_view(), name='signout'),
        path('verify-email', VerifyEmailView.as_view(), name='verify-email'),
        path('verify-token/<str:token>/', VerifyTokenView.as_view(), name='verify-token'),

]
