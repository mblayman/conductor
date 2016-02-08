import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']

# Other settings must explicitly opt-in for debug mode.
DEBUG = False

ALLOWED_HOSTS = []
