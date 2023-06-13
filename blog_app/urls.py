from django.contrib import admin
from django.urls import re_path, path
from django.conf.urls.static import static
from django.conf import settings as SETTINGS
from django.conf.urls import include

from general import views as general_views


urlpatterns = [
    # Admin url
    re_path(r'^86d80e04-4f25-4f27-a547-21cf5cb414f3/', admin.site.urls),

    # Registration urls
    path('accounts/register/', general_views.SkipEmailVerificationRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.default.urls')),


    re_path(r'^$', general_views.dashboard, name='dashboard'),
    re_path(r'^blogs/', include('blogs.urls', namespace="blogs")),

] + static(SETTINGS.STATIC_URL, document_root=SETTINGS.STATIC_ROOT) + static(SETTINGS.MEDIA_URL, document_root=SETTINGS.MEDIA_ROOT)
