#!/bin/bash
pyinstaller  -i ../logo/logo.ico --hidden-import=ijson --hidden-import=PySimpleGUI -F ../jsontosqlitegui.py -w