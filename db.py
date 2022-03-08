import psycopg2
import json
import config


class DataBase:
    async def get_lessons(self):
        connect = psycopg2.connect(
            database=config.DB_NAME,  
            user=config.DB_USER, 
            password=config.DB_PASSWORD,
            host=config.DB_HOST, 
            port=config.DB_PORT
        )   

        cursor = connect.cursor()


        cursor.execute('''
            SELECT * 
            FROM lesson_
        ''')
        arr = {}

        for x in cursor.fetchall():
            if arr.get(f"{x[0]}||{x[2]}") == None:
                arr[f"{x[0]}||{x[2]}"] = list()
            arr[f"{x[0]}||{x[2]}"].append(x)

        with open("data/lessons.json", "w", encoding="utf-8") as f:
            json.dump(arr, f, indent=4, ensure_ascii=False)
        connect.close()
w = DataBase()