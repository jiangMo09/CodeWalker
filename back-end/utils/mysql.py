import mysql.connector
from utils.load_env import HOST, USER, PASSWORD, NAME

dbconfig = {
    "host": HOST,
    "user": USER,
    "password": PASSWORD,
    "database": NAME,
}

pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=80, **dbconfig
)
# pool_size 15 from https://repost.aws/knowledge-center/rds-mysql-max-connections


def get_db_connection():
    connection = pool.get_connection()
    return connection


def execute_query(connection, query, values=None, fetch_method="fetchone"):
    with connection.cursor(dictionary=True) as cursor:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        fetch_function = getattr(cursor, fetch_method)
        result = fetch_function()

        if not query.lstrip().upper().startswith("SELECT"):
            connection.commit()

    return result


def get_db():
    connection = get_db_connection()
    try:
        yield connection
    finally:
        connection.close()
