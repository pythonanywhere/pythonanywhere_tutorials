from django.conf.urls.defaults import patterns, include, url

from server.renderer.views import render_view
from server import settings

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
        
    url(r'^(.*)$', render_view, name='render_view')
)


