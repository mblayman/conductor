#!/usr/bin/env bash

if [ -n "${CI}" ]; then
    VENV=venv/bin/
fi

${VENV}shiv \
    --compressed \
    -p '/usr/bin/env python3' \
    -o conductor-${CIRCLE_SHA1}.pyz \
    -e conductor.main:main \
    . -r requirements.txt
