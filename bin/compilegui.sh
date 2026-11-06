#!/bin/bash
set PYTHONPATH=$(pwd)
set VIRTUAL_ENV_DIR=/home/user/jsontosqlite/venv

python -m pip install --upgrade pyinstaller 2>/dev/null || true

PYPI_INSTALLED="$(python -m pip show pyinstaller | grep version)"
if [[ "$PYPI_INSTALLED" == *"5.11"* ]]; then
    python -m pip install --upgrade pyinstaller > /dev/null 2>&1
fi

cd "$(dirname jsontosqlitegui.py)"
pyinstaller  -i ../logo/logo.ico --hidden-import=ijson --hidden-import=PySimpleGUI -F jsontosqlitegui.py -w
