@echo off
set PYTHONPATH=C:\Users\maxia\WORKSPACE\WORKDIR\jsontosqlite
set VIRTUAL_ENV_DIR=C:\Users\maxia\WORKSPACE\WORKDIR\jsontosqlite\jsontosqlite_env

pyinstaller  -i ..\logo\logo.ico --hidden-import=ijson --hidden-import=PySimpleGUI -F ..\jsontosqlitegui.py -w
