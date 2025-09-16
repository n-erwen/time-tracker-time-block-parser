#!/usr/bin/python3
import csv
import sqlite3
import sys

"""
here i'm going to write records into the SQLite DB
records must be in csv format
"""

DB_NAME = 'time_blocks'

def connect_to_database():
    connection = sqlite3.connect(DB_NAME + '.db')
    return connection


def setup_database(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS time_block(
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT NOT NULL,
start_timestamp TEXT,
end_timestamp TEXT,
duration_mins INTEGER,
description TEXT,
details TEXT,
break_duration_mins INTEGER,
completed BOOLEAN NOT NULL CHECK (mycolumn IN (0, 1))
)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS tag(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL
)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS time_block_tag(
time_block_id INTEGER,
tag_id INTEGER,
FOREIGN KEY(time_block_id) REFERENCES time_block(id),
FOREIGN KEY(tag_id) REFERENCES tag(id)
)""")


def insert_time_block_record(connection, row):
    cursor = connection.cursor()
    query = f"""INSERT INTO time_block(
start_timestamp, end_timestamp, duration_mins, 
description, details, break_duration_mins, completed
) VALUES (\"{row['date']}\", 
{'"' + row['start'] + '"' if row['start'] else 'NULL'}, 
{'"' + row['end'] + '"' if row['end'] else 'NULL'}, 
{row['duration_mins'] if row['duration_mins'] else 'NULL'}, 
\"{row['description']}\",
\"{row['details']}\",
{row['break_duration_mins']}, 
{row['completed']})"""
    cursor.execute(query)
    return cursor.lastrowid


def insert_tag_record(connection, tag_name):
    cursor = connection.cursor()
    maybe_existing_tag_record = cursor.execute(f"""SELECT id, name
FROM tag
WHERE name = \"{tag_name}\"""").fetchone()
    if maybe_existing_tag_record:
        return maybe_existing_tag_record[0]
    else:
        cursor.execute(f"""INSERT INTO tag(name)
    VALUES (\"{tag_name}\")""")
        return cursor.lastrowid


def insert_time_block_tag_record(connection, time_block_id, tag_id):
    cursor = connection.cursor()
    cursor.execute(f"""INSERT INTO time_block_tag(time_block_id, tag_id)
VALUES ({time_block_id}, {tag_id})
""")
    return cursor.lastrowid


def insert_records(connection, csv_dict_reader):
    try:
        num_rows_inserted = 0
        for csv_row in csv_dict_reader:
            time_block_record_id = insert_time_block_record(connection, csv_row)
            for tag in csv_row['tags'].split('\n'):
                tag_record_id = insert_tag_record(connection, tag[1:])
                insert_time_block_tag_record(connection, time_block_record_id, tag_record_id)
            num_rows_inserted += 1
        db_conn.commit()
        return num_rows_inserted
    except Exception as e:
        db_conn.rollback()
        raise e


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('CSV file name must be provided')
    input_file_names = sys.argv[1:]
    db_conn = connect_to_database()
    total_num_rows_inserted = 0
    try:
        setup_database(db_conn)
        for file_name in input_file_names:
            with open(file_name, 'r') as file:
                reader = csv.DictReader(file)
                total_num_rows_inserted += insert_records(db_conn, reader)
    finally:
        print(total_num_rows_inserted, 'rows inserted')
        print('Closing connection')
        db_conn.close()


