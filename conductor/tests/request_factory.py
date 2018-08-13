from typing import Any

from django import test
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest


class RequestFactory(test.RequestFactory):
    def authenticated_get(
        self, user: settings.AUTH_USER_MODEL, **kwargs: Any
    ) -> HttpRequest:
        request = self.get(**kwargs)
        request.user = user
        return request

    def get(self, path: str = "/", session: bool = False, **kwargs: Any) -> HttpRequest:
        """Override the default get to avoid providing a meaningless path."""
        request = super().get(path, **kwargs)
        request.user = AnonymousUser()
        request.query_params = request.GET

        if session:
            middleware = SessionMiddleware()
            middleware.process_request(request)
            request.session.save()

        return request

    def authenticated_post(
        self, user: settings.AUTH_USER_MODEL, **kwargs: Any
    ) -> HttpRequest:
        request = self.post(**kwargs)
        request.user = user
        return request

    def post(
        self,
        path: str = "/",
        format: str = "multipart",
        session: bool = False,
        **kwargs: Any
    ) -> HttpRequest:
        """Override the default post to avoid providing a meaningless path."""
        request = super().post(path, format=format, **kwargs)
        request.user = AnonymousUser()

        if session:
            middleware = SessionMiddleware()
            middleware.process_request(request)
            request.session.save()

        return request
