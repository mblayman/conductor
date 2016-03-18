from rest_framework.renderers import JSONRenderer
from rest_framework_jwt import views as jwt_views


class ObtainJSONWebToken(jwt_views.ObtainJSONWebToken):
    """Shim the JWT view to use the default JSON renderer."""
    renderer_classes = (JSONRenderer,)
