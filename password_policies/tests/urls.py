from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^password/', include('password_policies.urls')),
)
