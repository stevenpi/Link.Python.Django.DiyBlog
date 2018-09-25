from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
