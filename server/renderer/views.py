# Copyright (c) 2011 Resolver Systems Ltd.
# All Rights Reserved
#

from docutils.core import publish_parts
import os

from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic.simple import redirect_to


CONTENT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ), 
        '..', '..',
        "content",
    )
)



def render_view(request, path):
    if path == '':
        return redirect_to(request, reverse("render_view", args=['index']))
        
    filename = os.path.abspath(os.path.join(CONTENT_DIR, path + '.txt'))
    if not os.path.exists(filename) or not filename.startswith(CONTENT_DIR):
        raise Http404()
        
    with open(filename, "r") as f:
        contents = f.read()

    parts = publish_parts(source=contents, writer_name="html4css1")
    return render_to_response(
        "tutorial_base.html",
        {
            "title": __tidy_html(parts["title"]),
            "body": __tidy_html(parts["body"]),
        }
    )



def __tidy_html(html):
    return html.replace("--", "&mdash;")


