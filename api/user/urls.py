from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# register the ViewSets with for each API objct type
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    path("", include(router.urls)), # /user
]

# leaderboard - no need this part because @action in views.py/CustomerUserViewSet will create path for it
# urlpatterns += [
#     path('leaderboard/', views.CustomerUserViewSet.as_view({'get': 'leaderboard'}), name='leaderboard')
# ]