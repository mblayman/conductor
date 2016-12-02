from rest_framework.test import APIRequestFactory, force_authenticate


class RequestFactory(APIRequestFactory):

    def authenticated_get(self, user, **kwargs):
        request = self.get(**kwargs)
        request.user = user
        force_authenticate(request, user)
        return request

    def get(self, path='/', **kwargs):
        """Override the default get to avoid providing a meaningless path."""
        return super(RequestFactory, self).get(path, **kwargs)

    def post(self, path='/', format='json', **kwargs):
        """Override the default post to avoid providing a meaningless path."""
        return super(RequestFactory, self).post(path, format=format, **kwargs)
