"""
URL configuration for gamification-tool project.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

# Patterns for each application's endpoints.
# The way Django's ModelViewSets work along with having to collect routes from each application
# doesn't allow for collecting each separate application's URLs in one path
# because it only assigns the first set of routes assigned to that path.
# This results in the project having endpoint paths such as '/users/users/...'
urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("user.urls")),
    path("leaderboard/", include("leaderboard.urls")),
    path('quiz/', include('quiz.urls')),
    path('memory-game/', include('memory_game.urls')),
    path("marketplace/", include("marketplace.urls")),
    path("checkins/", include("locations.urls")),
]

# Additional auth urls
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

# URLs for static and media if in dev environment
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
