from django.urls import path



from .views import CreateProfileView

urlpatterns = [
    path('createprofile/', CreateProfileView.as_view(), name="createprofile")

]