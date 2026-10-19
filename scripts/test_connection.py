from snowflake_connection import get_connection

with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_ROLE()")
        print(cursor.fetchone())
