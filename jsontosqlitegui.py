#!/usr/bin/env python
"""
    Flex Cosmos data management
    __author__ = "Massimo Iannuzzi"
    __copyright__ = "free use"
    __license__ = "MIT License"
    __maintainer__ = "Massimo Iannuzzi"
    __email__ = "max.iannuzzi@gmail.com"
"""

from _version import __version__
from lib.jsontosqlitelib import *
from globalmessages.globalmessages import *
from lib.guiutilities import *
import PySimpleGUI as sg
from sqlite3 import DatabaseError


collapse_database_export = [
    [
        sg.Input(sg.user_settings_get_entry('-databasenameexport-', ''), readonly=True, key='-DB-FILE-TABLE-EXPORT-')
        ,sg.FileBrowse(file_types=(("Sqlite database", "*.*"),), key='-DB-FILE-BROWSER-EXPORT-')

    ],
    [
        sg.Combo(['Press Get table list'],expand_x=True,readonly=True,key='-COMBO-TABLE-EXPORT-',default_value="Press Get table list")
        ,sg.B('Get table list', key='-GET-LIST-TABLE-'),
    ]
]

collapse_database_import = [
    [
         sg.Input(sg.user_settings_get_entry('-databasename-', ''), readonly=True, key='-DB-FILE-NEW-DATABASE-')
        ,sg.FileBrowse(file_types=(("Sqlite database", "*.*"),), key='-DB-FILE-BROWSER-')
    ]
]

collapse_new_database = [
    [
        sg.InputText(key='-DATABASENAME-', enable_events=True)
    ]
]

collapse_button_import = [
    [
    sg.B('Import', key='-BOTTON-IMPORT-'), sg.B('Exit', key='-BOTTON-EXIT-IMPORT-')
    ]
]

collapse_button_export = [
    [
        sg.B('Export', key='-BOTTON-EXPORT-'), sg.B('Exit', key='-BOTTON-EXIT-EXPORT-')
    ]
]

collapse_json_import = [
    [sg.Text('Select the json file to import:')],
    [
        sg.Input(sg.user_settings_get_entry('-filename-', ''), readonly=True,key='-FILE-JSON-INPUT-')
        , sg.FileBrowse(file_types=(("Json Files", "*.json"),))
    ]
]


layout = [
    [collapse(sg,collapse_json_import,True,'-JSON-IMPORT-')],
    [
        sg.Radio('New Database', "TYPEDATABASE", enable_events=True, default=True, key='-R1-')
        ,sg.Radio('Select Database', "TYPEDATABASE", enable_events=True, default=False, key='-R2-')
        ,sg.Radio('Export Table', "TYPEDATABASE", enable_events=True, default=False, key='-R3-')
    ],
    [sg.Text('Database:',key='-DB-TEXT-LABEL-',visible=True)],
    [collapse(sg,collapse_database_import,False,'-IMPORT-DATABASE-')],
    [collapse(sg,collapse_new_database,True,'-NEW-DATABASE-')],
    [collapse(sg,collapse_database_export,False,'-EXPORT-DATABASE-')],
    [collapse(sg,collapse_button_import,True,'-IMPORT-BUTTON-')],
    [collapse(sg,collapse_button_export,False,'-EXPORT-BUTTON-')],
    [sg.Checkbox('Open the database folder after closing the program', default=False , key='-OPENDIR-')]

]

window = sg.Window(f'JsonToSqlite ver {__version__}', layout)

databasename = None
path_file_json = None
while True:
    event, values = window.read()
    if (event in (sg.WINDOW_CLOSED, '-BOTTON-EXIT-IMPORT-')) or (event in (sg.WINDOW_CLOSED, '-BOTTON-EXIT-EXPORT-')):
        break
    elif event in ('-R3-'):
        type_db = values['-R3-']
        if type_db:
            window['-NEW-DATABASE-'].update(visible=False)
            window['-IMPORT-DATABASE-'].update(visible=False)
            window['-JSON-IMPORT-'].update(visible=False)
            window['-IMPORT-BUTTON-'].update(visible=False)
            window['-EXPORT-DATABASE-'].update(visible=True)
            window['-EXPORT-BUTTON-'].update(visible=True)
        continue
    elif event in ('-R2-'):
        type_db = values['-R2-']
        if type_db:
            window['-NEW-DATABASE-'].update(visible=False)
            window['-EXPORT-DATABASE-'].update(visible=False)
            window['-EXPORT-BUTTON-'].update(visible=False)
            window['-IMPORT-DATABASE-'].update(visible=True)
            window['-IMPORT-BUTTON-'].update(visible=True)
            window['-JSON-IMPORT-'].update(visible=True)
        continue
    elif event in ('-R1-'):
        type_db = values['-R1-']
        if type_db:
            window['-IMPORT-DATABASE-'].update(visible=False)
            window['-EXPORT-DATABASE-'].update(visible=False)
            window['-EXPORT-BUTTON-'].update(visible=False)
            window['-NEW-DATABASE-'].update(visible=True)
            window['-IMPORT-BUTTON-'].update(visible=True)
            window['-JSON-IMPORT-'].update(visible=True)
        continue
    elif event in ('-DATABASENAME-'):
        val_input = values['-DATABASENAME-']
        regex = r"[^0-9a-zA-Z\_\.]"
        match = re.search(regex, val_input)
        if match:
            window.Element('-DATABASENAME-').Update(values['-DATABASENAME-'][:-1])
        continue
    elif event == '-BOTTON-IMPORT-':
        path_file_json = values['-FILE-JSON-INPUT-']
        type_db1 = values['-R1-']
        type_db2 = values['-R2-']

        if type_db1:
            databasename = values['-DATABASENAME-']

        if type_db2:
            databasename = values['-DB-FILE-NEW-DATABASE-']

        if path_file_json is None or len(path_file_json.strip()) <= 0:
            sg.popup('Warning!', 'Select a json file')
            continue

        sg.user_settings_set_entry('-filename-', values['-FILE-JSON-INPUT-'])

        if databasename is None or len(databasename.strip()) <= 0:
            sg.popup('Warning!', 'Insert the database name')
            continue

        sg.user_settings_set_entry('-databasename-', values['-DB-FILE-NEW-DATABASE-'])

        if check_file_name(path_file_json):
            sg.popup('Warning!', ERROR_FILE_NAME_WRONG)
            continue

        table_name = os.path.basename(os.path.splitext(path_file_json)[0])
        path_file_name_json = os.path.dirname(path_file_json)

        try:
            if type_db1:
                databasename = ''.join((path_file_name_json, os.path.sep, databasename))
                if os.path.exists(databasename):
                    responce = sg.popup_yes_no('The database already exists. Do you want to use it?')
                    if responce == "No":
                        continue

            import_file_json(path_file_json,databasename)

            sg.popup('Info', f'Import Done in database\n {databasename}')
            responce = sg.popup_yes_no('Do you want to import another file?')
            if responce == "Yes":
                continue
            else:
                database_path =  os.path.dirname(databasename)
                check_opendir = values['-OPENDIR-']
                if check_opendir:
                    open_folder(database_path)
                break

        except DatabaseError as e:
            sg.popup('Error!', str(e))
   
    elif event == '-GET-LIST-TABLE-':
        databasename = values['-DB-FILE-TABLE-EXPORT-']
        if databasename is None or len(databasename.strip()) <= 0:
            sg.popup('Warning!', 'Select the database from file')
            continue
        sg.user_settings_set_entry('-databasenameexport-', values['-DB-FILE-TABLE-EXPORT-'])
        table_list_combo = ['Select a table']
        tmp_table_list = get_table_list(databasename)
        table_list_combo.extend(tmp_table_list)
        window['-COMBO-TABLE-EXPORT-'].update(value='', values=table_list_combo)
        window['-COMBO-TABLE-EXPORT-'].update(value="Select a table")
        continue
    elif event == '-BOTTON-EXPORT-':
        databasename = values['-DB-FILE-TABLE-EXPORT-']
        if databasename is None or len(databasename.strip()) <= 0:
            sg.popup('Warning!', 'Select the database from file')
            continue
        table_name = values['-COMBO-TABLE-EXPORT-']
        if table_name in ('Press Get table list','Select a table'):
            sg.popup('Warning!', 'Select a correct table name')
            continue
        export_info = exportTableToJson(databasename,table_name)
        sg.popup('Info!', f'Export Done in file {export_info}')


window.close()