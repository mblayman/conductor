#/bin/bash
# A simple wrapper for manage.py to run it through honcho first.
honcho run python manage.py $@
