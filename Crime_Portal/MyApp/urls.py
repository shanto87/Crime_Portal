from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.login),
    path('index.html/', views.home),
    path('login.html/', views.login),
    path('aboutus.html/', views.aboutus),
    path('crimenews.html/', views.crimenews),
    path('localintelligence.html/', views.localintelligence),
    path('violencereporting.html/', views.violencereporting),
    path('wantedlist.html/', views.wantedlist),
    path('signup.html/', views.signup),
    path('userDashboard.html/', views.userDashboard),
    path('gd.html/', views.gd),
]

#urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
