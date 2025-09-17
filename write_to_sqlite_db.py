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
completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS tag(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
UNIQUE(name)
)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS time_block_tag(
time_block_id INTEGER,
tag_id INTEGER,
FOREIGN KEY(time_block_id) REFERENCES time_block(id),
FOREIGN KEY(tag_id) REFERENCES tag(id)
)""")

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

#   get all ids of existing rows in time_block
#   filter rows from csv where id is in existing rows
#   filter rows from csv where id is not in existing rows
#   update all existing rows
#   insert all non existing rows
#   get all tags
#   insert on conflict ignore for all tags
#   get all time block tag id associations
#   for each record
#     filter csv tags for tags which dont exist in associations
#     insert those tags
#     filter associations for tags which dont exist in csv
#     delete those tags


def execute_query_and_get_row_count(connection, query):
    cursor = connection.cursor()
    result = cursor.execute(query)
    return result.rowcount


def fetch_all_rows_from_query(connection, query):
    cursor = connection.cursor()
    result = cursor.execute(query)
    return result.fetchall()


def get_unique_tags_from_csv_rows(rows):
    return set([tag.replace('#', '') for row in rows for tag in row['tags'].split()])


def get_time_block_row_values_as_sql_str(row):
    values = [
        '"' + row['date'] + '"',
        '"' + row['start'] + '"' if row['start'] else 'NULL',
        '"' + row['end'] + '"' if row['end'] else 'NULL',
        row['duration_mins'] if row['duration_mins'] else 'NULL',
        '"' + row['description'] + '"',
        '"' + row['details'] + '"',
        row['break_duration_mins'],
        row['completed']
    ]
    return '(' + ', '.join(values) + ')'


def get_all_time_block_record_ids(connection):
    return [row[0] for row in fetch_all_rows_from_query(connection, 'SELECT id FROM time_block;')]


def get_time_block_tag_records_for_time_block_ids(connection):
    query = 'SELECT time_block_id, tag_id FROM time_block_tag'
    return [
        {
            'time_block_id': row[0],
            'tag_id': row[1]
        } for row in fetch_all_rows_from_query(query)
    ]


def get_tag_ids_for_names(connection, tags):
    row_values_str = '(' + ', '.join(tags) + ')'
    query = f"""SELECT id, name FROM tag
    WHERE name in {row_values_str}"""
    return [
        {'id': row[0], 'name': row[1]}
        for row in fetch_all_rows_from_query(connection, query)
    ]


def insert_time_block_records(connection, rows):
    row_values_str = ', '.join([
        get_time_block_row_values_as_sql_str(row) for row in rows
    ])
    query = f"""INSERT OR REPLACE INTO time_block(
date, start_timestamp, end_timestamp, duration_mins, 
description, details, break_duration_mins, completed
) VALUES {row_values_str}
RETURNING id;
"""

    return [row[0] for row in fetch_all_rows_from_query(connection, query)]


def insert_tag_records(connection, rows):
    tags = get_unique_tags_from_csv_rows(rows)
    row_values_str = ', '.join(['("' + tag + '")' for tag in tags])
    print(row_values_str)
    query = f"""INSERT OR IGNORE INTO tag(name)
    VALUES {row_values_str}
    """
    return execute_query_and_get_row_count(connection, query)


def update_time_block_tag_association_records(connection, rows):
    tag_records = get_tag_ids_for_names()


def insert_or_replace_time_block_records(connection, rows):
    existing_record_ids = get_all_time_block_record_ids(connection)
    rows_to_insert = [row for row in rows if row['id'] not in existing_record_ids]
    rows_to_replace = [row for row in rows if row['id'] in existing_record_ids]
    inserted_row_ids = insert_time_block_records(connection, rows_to_insert)
    for idx in range(len(rows_to_insert)):
        rows_to_insert[idx]['id'] = inserted_row_ids[idx]
    print(rows_to_insert)
    replaced_count = 0
    print('time_blocks: ' + str(len(inserted_row_ids)) + ' rows inserted, ' + str(replaced_count) + ' rows replaced')
    return rows_to_insert + rows_to_replace


def insert_or_update_records_from_csv_file(connection, file_name):
    with open(file_name, 'r') as file:
        rows = [{**row, 'id': int(row['id']) if row['id'] else None} for row in list(csv.DictReader(file))]
        insert_or_replace_time_block_records(connection, rows)
        tag_inserted_count = insert_tag_records(connection, rows)
        print('tag: ' + str(tag_inserted_count) + ' inserted')



if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('CSV file name must be provided')
    input_file_names = sys.argv[1:]
    db_conn = connect_to_database()
    try:
        print('Setting up database')
        setup_database(db_conn)
        for csv_file_name in input_file_names:
            insert_or_update_records_from_csv_file(db_conn, csv_file_name)
            # with open(file_name, 'r') as file:
            #     reader = csv.DictReader(file)
            # total_num_rows_inserted += insert_records(db_conn, reader)
        print('Committing changes')
        db_conn.commit()
    except Exception as e:
        print('Error occurred, rolling back changes')
        db_conn.rollback()
        raise e
    finally:
        print('Closing connection')
        db_conn.close()
