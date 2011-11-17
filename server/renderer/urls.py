# Copyright (c) 2011 Resolver Systems Ltd.
# All Rights Reserved
#

from django.conf.urls.defaults import *
from django.conf import settings

from anywhere.tutorial.views import render_tutorial_page, tutorial_root


urlpatterns = patterns('',

    url(
        '^tutorial/$',
        tutorial_root,
        name="tutorial_root"
    ),

    url(
        '^tutorial/(\d+)/$',
        render_tutorial_page,
        name="tutorial_page"
    ),
)
