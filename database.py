import sqlite3
import os

if __name__ == '__main__':
    try:
        conn = sqlite3.connect('./test.db')
    except:
        raise sqlite3.Error

    cursor = conn.cursor()
    sql_del = "DROP TABLE IF EXISTS tbl_test;"
    try:
        cursor.execute(sql_del)
    except:
        raise sqlite3.Error
    conn.commit()

    sql_create_tbl = (
        '''
        CREATE TABLE TEST
        (
        ID INT PRIMARY KEY NOT NULL ,
        
        
        
        )
        '''
    )

