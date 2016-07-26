from django.conf.urls import include, patterns, url

from password_policies.tests.views import TestHomeView


urlpatterns = patterns('',
                       url(r'^password/', include('password_policies.urls')),
                       url(r'^$', TestHomeView.as_view(), name='home'),
                       )
