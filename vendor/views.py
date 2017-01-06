from rest_framework import exceptions, status
from rest_framework.renderers import JSONRenderer
from rest_framework_json_api.exceptions import exception_handler
from rest_framework_jwt import views as jwt_views


def custom_exception_handler(exc, context):
    # Ember Data expects server side validation errors to be 422.
    if isinstance(exc, exceptions.ValidationError):
        exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    response = exception_handler(exc, context)
    return response


class ObtainJSONWebToken(jwt_views.ObtainJSONWebToken):
    """Shim the JWT view to use the default JSON renderer."""
    renderer_classes = (JSONRenderer,)


class RefreshJSONWebToken(jwt_views.RefreshJSONWebToken):
    """Shim the JWT view to use the default JSON renderer."""
    renderer_classes = (JSONRenderer,)
