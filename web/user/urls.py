from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# register the ViewSets for each API object type
router = DefaultRouter()
router.register(r'users', views.UserViewSet,)

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name = 'logout'),
    path("", include(router.urls)), # /user
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# leaderboard - no need this part because @action in views.py/CustomerUserViewSet will create path for it
# urlpatterns += [
#     path('leaderboard/', views.CustomerUserViewSet.as_view({'get': 'leaderboard'}), name='leaderboard')
# ]