from django.urls import path



from .views import CreateProfileView, UpdateProfileView

urlpatterns = [
    path('createprofile/', CreateProfileView.as_view(), name="createprofile"),
    path('updateprofile/', UpdateProfileView.as_view(), name="updateprofile"),

]