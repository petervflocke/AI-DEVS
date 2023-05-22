import sqlite3
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import json
import os
import chardet

class SQLiteHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_table_brain = 'brain'
        self.conn = None
        self.cursor = None
        self.create_connection_and_table()

    def create_connection_and_table(self):
        if not os.path.exists(self.db_name):
            self.conn = sqlite3.connect(self.db_name)
            self.create_table()
        else:
            self.conn = sqlite3.connect(self.db_name)
            if not self.check_table_exists(self.db_table_brain):
                self.create_table()
        self.cursor = self.conn.cursor()
        #self.conn.set_trace_callback(print)

    def check_table_exists(self, table_name):
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        return bool(self.cursor.fetchall())

    def create_table(self):
        query = f"""create virtual table {self.db_table_brain} using fts5(body);"""
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        data = {k: json.dumps(v) if isinstance(v, list) else v for k, v in data.items()}
        columns = ', '.join(data.keys())
        values = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query, list(data.values()))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def fuzzy_search_entities(self, search_for, threshold=80):
        search_for = search_for.strip('][').split(', ')
        self.cursor.execute(f"SELECT original_message, entities FROM {self.db_table_brain}")
        data = self.cursor.fetchall()

        matching_messages = []
        for original_message, entities in data:
            found = False
            print(original_message, entities)
            entities = entities.strip('][').split(', ')
            for entity in entities:
                for search_term in search_for:
                    if fuzz.ratio(entity, search_term) > threshold:
                        matching_messages.append(original_message)
                        found = True
                        break
                if found:
                    break
        print (matching_messages)
        return matching_messages


    def print_match(self, search_for):
        self.cursor.execute(f"SELECT body FROM {self.db_table_brain}")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"{row}")

    def print_select(self, select_txt):
        self.cursor.execute(f"{select_txt}")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"{row}")

    def print_data(self):
        self.cursor.execute(f"SELECT body FROM {self.db_table_brain}")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"{row}")


if __name__ == "__main__":
    
    LOAD = False

    DATABASE = os.path.dirname(os.path.abspath(__file__)) + "/brain01.db"
    print (DATABASE)
    handler = SQLiteHandler(DATABASE)

    if LOAD:
        rawdata = open('quotes.json', 'rb').read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        print (f"Encoding: {encoding}")

        with open('quotes.json', 'r', encoding=encoding) as f:
            data = json.load(f)

        for row in data:
            if row['quoteAuthor'] != '':
                handler.insert_data(handler.db_table_brain, {"body" : f"{row['quoteAuthor']} said: {row['quoteText']}"})

    #handler.print_data()
    handler.print_select("SELECT count (*) FROM brain")
    handler.print_select("SELECT * FROM brain WHERE body MATCH('Buddha happiness')")
    handler.close_connection()
