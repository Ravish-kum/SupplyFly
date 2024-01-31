from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import UserSignup, UserSignin, UserDetailsUpdate

urlpatterns = [

    path('signup/',UserSignup.as_view(), name='signup'),
    path('signin/', UserSignin.as_view() , name='signin'),
    path('updatedetails/', UserDetailsUpdate.as_view(), name='update'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
