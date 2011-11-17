# Copyright (c) 2011 Resolver Systems Ltd.
# All Rights Reserved
#


from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect

from mock import Mock, patch
import os

from resolver_test import ResolverViewTestCase

from server.renderer.views import render_view


class RenderViewTest(ResolverViewTestCase):
    
    @patch("server.renderer.views.os.path.exists")    
    def test_render_view_404s_for_nonexistent_file(self, mock_exists):
        mock_exists.return_value = False

        with self.assertRaises(Http404):
            render_view(self.request, '9')
        
        
    def test_render_view_404s_for_existing_file_outside_of_content_directory(self):
        
        with self.assertRaises(Http404):
            render_view(self.request, '../../README')
        
        
    @patch("server.renderer.views.os.path.exists")          
    @patch("server.renderer.views.publish_parts")
    @patch("server.renderer.views.render_to_response")        
    def test_render_view_renders_rst_sensibly(self, mock_render, mock_publish_parts, mock_exists):
        mock_exists.return_value = True
        mock_open = Mock()
        read_results = "The rest contents"
        mock_open.return_value.__enter__ = Mock()
        mock_open.return_value.__enter__.return_value.read.return_value = read_results
        mock_open.return_value.__exit__ = Mock()

        mock_publish_parts.return_value = {
            "title": "I am a dashing -- title",
            "body": "<div>I am a processed rest body with double --s</div>"
        }


        orig_open = open
        __builtins__['open'] = mock_open
        try:
            response = render_view(self.request, "foo")
        finally:
            __builtins__['open'] = orig_open

        contents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'content'))   
        self.assertCalledOnce(mock_open, os.path.join(contents_dir, 'foo.txt'), "r")
        self.assertCalledOnce(mock_publish_parts, source=read_results, writer_name="html4css1")

        self.assert_render_template_was(mock_render, "tutorial_base.html")
        self.assertRenderedWith(mock_render, "title", "I am a dashing &mdash; title")
        self.assertRenderedWith(mock_render, "body", "<div>I am a processed rest body with double &mdash;s</div>")


    def test_render_view_handles_root_request_sensibly(self):
        self.request.META['QUERY_STRING'] = ''
        
        response = render_view(self.request, '')

        self.assertIsInstance(response, HttpResponsePermanentRedirect)
        self.assertEquals(
            response['Location'],
            reverse('render_view', args=['index'])
        )






