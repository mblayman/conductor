#!/usr/bin/env bash

# Clean old build.
rm -rf dist conductor.pyz

# Put all the code in dist.
pip install -r requirements.txt --target dist/
pip install . --target dist/

shiv --site-packages dist --compressed \
    -p '/usr/bin/env python3' -o conductor.pyz -e conductor.main
