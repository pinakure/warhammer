from django.conf.urls.static    import static
from django.conf                import settings
from django.contrib             import admin
from django.contrib.auth.views  import LoginView
from django.urls                import include,path
from .views import *

urlpatterns = [
    path('admin/'           , admin.site.urls),
    path(''                 , view_main          , name='view_main'),
    path('accounts/login/'  , view_login         , name="view_login"),
    path('logout/'          , view_logout        , name='view_logout'),
    path('get/'             , view_get           , name='view_get'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
