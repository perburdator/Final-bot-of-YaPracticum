import sqlite3

from other import DB_NAME, TABLE_NAME


def create_db(database_name=DB_NAME):
    connection = sqlite3.connect(database_name)
    connection.close()


def execute_query(sql_query, data=None, db_path=DB_NAME):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)
        connection.commit()


def execute_selection_query(sql_query, data=None, db_path=DB_NAME):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.close()
    return rows


def create_table(table_name):
    sql_query = f'''CREATE TABLE IF NOT EXISTS {table_name}(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                tts_symbols INTEGER,
                stt_blocks INTEGER)'''
    execute_query(sql_query)


def insert_row(user_id, message, tts_symbols):
    sql_query = 'INSERT INTO messages (user_id, message, tts_symbols)VALUES (?, ?, ?)'
    execute_query(sql_query, [user_id, message, tts_symbols])


def count_all_symbol(user_id):
    sql_query = 'SELECT SUM(tts_symbols) FROM messages WHERE user_id=?'
    data = execute_selection_query(sql_query, [user_id])[0]

    if data and data[0]:
        return data[0]

    else:
        return 0


def count_all_limits(user_id):
    sql_query = 'SELECT SUM(stt_blocks) FROM messages WHERE user_id=?'
    data = execute_selection_query(sql_query, [user_id])[0]

    if data and data[0]:
        return data[0]

    else:
        return 0
