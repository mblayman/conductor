#!/usr/bin/env bash

VENV=venv/bin/

# Clean old build.
rm -rf dist conductor.pyz

# Put all the code in dist.
pip install . -r requirements.txt --target dist/

${VENV}shiv --site-packages dist --compressed \
    -p '/usr/bin/env python3' \
    -o conductor-${CIRCLE_SHA1}.pyz \
    -e conductor.main
