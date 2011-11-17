from django.conf.urls.defaults import patterns, include, url

from server.renderer.views import render_view


urlpatterns = patterns('',
    url(r'^(.*)$', render_view, name='render_view')
)
