from ast import literal_eval
import psycopg2
from misc.get_dollar import get_cur_value
from datetime import datetime


def Create_Table(conn):
    cursor = conn.cursor()
    cursor.execute(
    """--sql
        CREATE TABLE IF NOT EXISTS MAIN_TABLE
        (
            ID varchar(255) primary key,
            Order_ID varchar(255),
            price_in_usd varchar(255),
            price_in_rub varchar(255),
            due_to varchar(255)
        );
    """)
    conn.commit()
    cursor.close()

def Database_update(conn, data: str):

    dollar = get_cur_value("R01235").replace(',', '.')

    cursor = conn.cursor()
    data = literal_eval(data)
    for i in data:
        if len(i) != 4:
            continue
        
        cursor.execute(
            f"""--sql
                INSERT INTO MAIN_TABLE(ID, Order_ID, price_in_usd, price_in_rub, due_to)
                VALUES(
                    {i[0]},
                    {i[1]},
                    {i[2]},
                    {str(int(i[2]) * float(dollar))},
                    '{i[3]}'
                )
                ON Conflict(id) DO UPDATE
                    SET
                    Order_ID = {int(i[1])},
                    price_in_usd = {i[2]},
                    price_in_rub = {str(int(i[2]) * float(dollar))},
                    due_to = '{i[3]}';
            """
        )
                        

    conn.commit()
    cursor.close()