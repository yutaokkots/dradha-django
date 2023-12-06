from django.urls import path



from .views import ProfileView, UpdateProfileView

urlpatterns = [
    path('createprofile/', ProfileView.as_view(), name="createprofile"),
    path('updateprofile/', UpdateProfileView.as_view(), name="updateprofile"),
    path('u/<str:userslug>/', ProfileView.as_view(), name="getprofile"), 
]