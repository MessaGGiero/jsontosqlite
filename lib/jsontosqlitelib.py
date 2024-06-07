#!/usr/bin/env python
"""
    Flex Cosmos data management
    __author__ = "Massimo Iannuzzi"
    __copyright__ = "free use"
    __license__ = "MIT License"
    __maintainer__ = "Massimo Iannuzzi"
    __email__ = "max.iannuzzi@gmail.com"
"""
import json
import sqlite3
import ijson
import re
import os
import sys,subprocess
import ast
import decimal
# Error Level
__errEnv = -1


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def create_table_stmt(table_name, columns:list):
    """
    :param table_name: Table Name
    :param columns: List columns
    :return: Str --> Create statment
    """
    stmt = ''
    column_str_list = ''
    first = True
    columns.sort()
    for col in columns:
        column_str_list += f"{col+' varchar' if first else ','+col+' varchar'}"
        first = False

    create_table_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str_list})"
    return create_table_stmt

def create_alter_table_stmt(table_name:str,column:str):
    """
    
    :param table_name: Table Name
    :param column:  column
    :return: str Statment
    """
    create_table_stmt = f"ALTER TABLE {table_name} ADD COLUMN {column} varchar"

    return create_table_stmt

def create_insert_row(table_name:str, current_list_columns:list, data:dict):
    """

    :param table_name: Table name
    :param current_list_columns: Current list columns in table target
    :param data: Dictionary datata
    :return: create_statmet, values ( statment str and list values)
    """
    insert_statmet = ''
    first = True
    positional_params = ''
    columns = ''
    values = []

    for col in current_list_columns:
        columns += f"{ col if first else ','+col}"
        positional_params += f"{ '?' if first else ',?'}"
        first = False
        column_value = None
        try:
            column_value = data[col]
        except KeyError:
            pass
        if isinstance(column_value,list) or isinstance(column_value,set) or isinstance(column_value,dict):
            #values.append(str(column_value))
            column_value = json.dumps(column_value,cls=DecimalEncoder)
            values.append(str(column_value))
        else:
            values.append(str(column_value))

    insert_statmet = f"insert into {table_name} ({columns}) values ({positional_params})"

    return insert_statmet, values

def merge_list_columns(current_list_columns:list,list_columns_to_work:list):
    """

    :param current_list_columns: Actual table column list in use
    :param list_columns_to_work: List from current document managed
    :return: Merged list sorted
    """
    len_list_current = len(list_columns_to_work)
    len_list_work = len(current_list_columns)

    if len_list_work == 0:
        return current_list_columns

    if len_list_current == 0:
        return list_columns_to_work

    current_list_columns.sort()
    list_columns_to_work.sort()

    out_list = list(set(current_list_columns + list_columns_to_work))
    out_list.sort()

    return out_list

def check_and_crate_alter_table_stmt(table_name:str, current_list_columns:list, new_list_columns_to_work:list):

    len_list_current = len(current_list_columns)
    len_list_work = len(new_list_columns_to_work)

    list_alter_stmt = []

    if len_list_work == 0 or len_list_current == 0:
        return list_alter_stmt

    for nc in new_list_columns_to_work:
        if nc not in current_list_columns:
            list_alter_stmt.append(create_alter_table_stmt(table_name,nc))

    return list_alter_stmt

def open_folder(path):
    i=0
    if 'win' in sys.platform:
        subprocess.call('explorer {}'.format(path.replace('/','\\')),shell=True)

def import_file_json(json_file, database_name):

    table_name = os.path.basename(os.path.splitext(json_file)[0])

    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    with open(json_file, 'rb') as input_file1:
        current_table_columns = []
        jsonobj1 = ijson.items(input_file1, 'item')
        i=0
        for f1 in jsonobj1:
            if i == 0:
                current_table_columns = list(f1.keys())
                statment_create_table = create_table_stmt(table_name, current_table_columns)
                c.execute(statment_create_table)
            i += 1

            alter_table_statments = check_and_crate_alter_table_stmt(table_name, current_table_columns, list(f1.keys()))
            if len(alter_table_statments) > 0:
                for alter_stmt in alter_table_statments:
                    c.execute(alter_stmt)
                current_table_columns = merge_list_columns(current_table_columns,list(f1.keys()))

            insert_statmet, values = create_insert_row(table_name, current_table_columns,f1)
            c.execute(insert_statmet,values)

    conn.commit()

def get_table_list(database_name):
    """
    :param database_name:
    :return: list tables name
    """
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    ret_list_table = [name[0] for name in c.fetchall()]
    c.close()
    return ret_list_table

def exportTableToJson(database_name,table_name):
    """
    :param database_name:
    :param table_name:
    :return:
    """
    dirname = os.path.dirname(database_name)
    json_file_export = f'{dirname}/{table_name}.json'
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    query = f"SELECT * FROM '{table_name}'"
    c.execute(query)
    first_item = True
    # fetchall as result
    with open(json_file_export, 'w') as out:
        out.write('[')
        while (row:=c.fetchone()) is not None:
            json_out = {}
            columns = list(c.description)
            json_out = dict((c.description[i][0], value) for i, value in enumerate(row))
            if first_item:
                out.write(json.dumps(json_out,indent=4))
                first_item = False
            else:
                out.write(",\n" + json.dumps(json_out,indent=4))
        out.write("]")
    # close connection
    conn.close()
    return  json_file_export

def exportTableToJson(database_name,table_name):
    """
    :param database_name:
    :param table_name:
    :return:
    """
    dirname = os.path.dirname(database_name)
    json_file_export = f'{dirname}/{table_name}.json'
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    query = f"SELECT * FROM '{table_name}'"
    c.execute(query)
    first_item = True
    # fetchall as result
    with open(json_file_export, 'w') as out:
        out.write('[')
        while (row:=c.fetchone()) is not None:
            json_out = {}
            columns = list(c.description)
            json_out = dict((c.description[i][0], leteral_manage(value)) for i, value in enumerate(row))
            if first_item:
                out.write(json.dumps(json_out,indent=4))
                first_item = False
            else:
                out.write(",\n" + json.dumps(json_out,indent=4))
        out.write("]")
    # close connection
    conn.close()
    return  json_file_export

def leteral_manage(value):
    ret_value = None
    try:
        ret_value = ast.literal_eval(value)
    except:
        ret_value = value

    return ret_value

def check_file_name(file_name:str):
    """

    :param file_name: File name to check
    :return:
    """
    regex1 = r"[-$&!#\s]+"
    regex2 = r"^[0-9]+"
    base_file_name =  os.path.basename(os.path.splitext(file_name)[0])
    match1 = re.search(regex1, base_file_name)
    match2 = re.search(regex2, base_file_name)

    if match1 or match2:
        return True
    else:
        return False

#print(crete_table('MyTable',['campo1','campo2','campo3']))
#print(crete_table('MyTable',['campo1']))

#print(insert_row('MyTable',['campo1','campo2','campo3'], {"campo1": 1,"campo2":'ciao',"campo3":{"a":"pippo"}}))
#print(merge_ordered_list_columns(['campo3','campo4','campo3'],['campo1','campo2','campo5']))