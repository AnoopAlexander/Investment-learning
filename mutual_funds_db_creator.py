import argparse
import re
import sqlite3
import numpy as np 
import pandas as pd 

def arg_parser():
    '''
    Use argparse to parse and return args
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename',help='Provide csv file for parsing')
    parser.add_argument('-d','--database',help='.db file name')
    args = parser.parse_args()
    return args

def create_connection(db_file):
    '''
    Create an sql connection for db file
    :params db_file: database fie
    :return: Connection object or None
    '''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return conn

def create_table_statement(table_name):
    '''
    Create a sql query to create table 
    '''
    statement = "CREATE TABLE "+str(table_name)+" (date date, nav float)"
    return statement

def main():
    '''
    The main code to be executed
    '''
    args = arg_parser()
    #print(args.filename)
    try:
        base_db = pd.read_csv(args.filename)
        #print(base_db.head())
    except Exception as e:
        print(e)
        pass
    insert_db = pd.DataFrame()
    insert_db['date'] = base_db.Date
    insert_db['nav'] = base_db.Close
    #print(insert_db.head())
    table_name = args.filename.split('.')[0]
    #print(table_name)
    conn = create_connection(args.database)
    statement = create_table_statement(table_name)
    c = conn.cursor()
    try:
        c.execute(statement)
        print("Execute successful")
    except Exception as e:
        print(e)
        pass
    insert_db.to_sql(table_name,conn,if_exists='append', index = False)
    
main()