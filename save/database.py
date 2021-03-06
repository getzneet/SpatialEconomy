from sqlite3 import connect, OperationalError
from os import path
from collections import OrderedDict


class Database(object):

    def __init__(self, folder="../data", name="db"):

        self.db_path = "{}/{}.db".format(folder, name)

        self.connexion = connect(self.db_path)
        self.cursor = self.connexion.cursor()

        self.is_close = 0

    def create_table(self, table_name, columns):

        assert type(columns) == dict or type(columns) == OrderedDict, \
            "Columns type should be dict such dict or OrderedDict with as keys names and as values types in string"

        query = "CREATE TABLE `{}` (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT, ".format(table_name)

        for key, value in columns.items():

            query += "`{}` {}, ".format(key, value)

        query = query[:-2]
        query += ")"
        self.write(query)
        # self.connexion.commit()

    def remove_table(self, table_name):

        q = "DROP TABLE `{}`".format(table_name)
        self.cursor.execute(q)
        # self.connexion.commit()

    def has_table(self, table_name):

        already_existing = self.get_tables_names()

        return table_name in already_existing

    def get_tables_names(self):

        if path.exists(self.db_path):

            # noinspection SqlResolve
            already_existing = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

            if already_existing:

                already_existing = [i[0] for i in already_existing]
                already_existing.remove("sqlite_sequence")
                return already_existing

            else:
                return []

        else:

            return []

    def get_columns(self, table_name='data'):

        tuple_column = [(i[1], i[2]) for i in self.read("PRAGMA table_info({})".format(table_name)) if i[1] != "ID"]
        dic_column = OrderedDict()

        for i, j in tuple_column:

            dic_column[i] = j

        return dic_column

    def read(self, query):

        try:
            self.cursor.execute(query)
        except OperationalError as e:
            print("Error with query:", query)
            raise e

        content = self.cursor.fetchall()

        return content

    def write(self, query):

        self.cursor.execute(query)

    def read_n_rows(self, columns, table_name='data'):

        read_query = "SELECT "

        for i in columns.keys():
            read_query += "`{}`, ".format(i)

        read_query = read_query[:-2]
        read_query += " from {}".format(table_name)

        return self.read(read_query)

    def write_n_rows(self, columns, array_like, table_name='data'):

        assert type(columns) == dict or type(columns) == OrderedDict, \
            "Columns type should be dict such dict or OrderedDict with as keys names and as values types in string"

        fill_query = "INSERT INTO '{}' (".format(table_name)

        for i in columns.keys():

            fill_query += "`{}`, ".format(i)

        fill_query = fill_query[:-2]
        fill_query += ") VALUES ("

        for i in range(len(columns)):
            fill_query += "?, "

        fill_query = fill_query[:-2]
        fill_query += ")"

        self.cursor.executemany(fill_query, array_like)
        # self.connexion.commit()

    def create_table_and_write_n_rows(self, columns, array_like, table_name='data'):

        assert type(columns) == dict or type(columns) == OrderedDict, \
            "Columns type should be dict such dict or OrderedDict with as keys names and as values types in string"

        create_table_query = \
            "CREATE TABLE `{}` (" \
            "ID INTEGER PRIMARY KEY, ".format(table_name)

        for key, value in columns.items():
            create_table_query += "`{}` {}, ".format(key, value)

        create_table_query = create_table_query[:-2]
        create_table_query += ")"

        fill_query = "INSERT INTO '{}' (".format(table_name)

        for i in columns.keys():

            fill_query += "`{}`, ".format(i)

        fill_query = fill_query[:-2]
        fill_query += ") VALUES ("

        for i in range(len(columns)):
            fill_query += "?, "

        fill_query = fill_query[:-2]
        fill_query += ")"

        self.cursor.execute(create_table_query)

        self.cursor.executemany(fill_query, array_like)

    def close(self):

        self.connexion.commit()
        self.connexion.close()

        self.is_close = 1

        # print("Database {} is closed.".format(self.db_path))

    def __del__(self):
        if not self.is_close:

            self.close()
