import sqlite3


class Database:
    def __init__(self, path_to_db="data/Users.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(
        self,
        sql: str,
        parameters: tuple = None,
        fetchone=False,
        fetchall=False,
        commit=False,
    ):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE "Users" (
	        "id"	INTEGER NOT NULL UNIQUE,
	        "ism"	TEXT,
	        "viloyat"	TEXT
            );
        """

        self.execute(sql, commit=True)

    def create_table_tests(self):
        sql = """
        CREATE TABLE "Testlar" (
            "id"	INTEGER NOT NULL,
            "file_id"	TEXT,
            "fan"	INTEGER NOT NULL,
            "javoblar"	TEXT,
            "tarif"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """

        self.execute(sql, commit=True)

    def create_table_results(self):
        sql = """
        CREATE TABLE "Results" (
            "user_id"	INTEGER NOT NULL,
            "test_id"	INTEGER,
            "bal"	REAL,
            "fan_id"    INTEGER
        );
        """

        self.execute(sql, commit=True)

    def create_table_fanlar(self):
        sql = """
        CREATE TABLE "Fanlar" (
            "id"	INTEGER,
            "nomi"	TEXT UNIQUE,
            "tur"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """

        self.execute(sql, commit=True)

    def create_table_temp(self):
        sql = """
        CREATE TABLE Temp(
            id  INTEGER UNIQUE,
            datetime    TEXT,
            test_id     INTEGER,
            fan_id  INTEGER,
            status  INTEGER
        );
        """

        self.execute(sql=sql, commit=True)

    # Users

    def select_all_users(self):
        return self.execute(sql="SELECT * FROM Users WHERE TRUE", fetchall=True)

    def select_user_by_id(self, id):
        return self.execute(
            sql="SELECT * FROM Users WHERE id = ?", parameters=(id,), fetchone=True
        )

    def add_user(self, id, ism, viloyat):
        self.execute(
            sql="INSERT INTO Users(id, ism, viloyat) VALUES(?, ?, ?)",
            parameters=(id, ism, viloyat),
            commit=True,
        )

    def update_ism(self, id, ism):
        self.execute(
            sql="UPDATE Users SET ism = ? WHERE id = ?",
            parameters=(ism, id),
            commit=True,
        )

    def update_vil(self, id, vil):
        self.execute(
            sql="UPDATE Users SET viloyat = ? WHERE id = ?",
            parameters=(vil, id),
            commit=True,
        )

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users", fetchone=True)

    # Testlar

    def add_test(self, file_id, fan, javoblar, tarif):
        self.execute(
            sql="INSERT INTO Testlar(file_id, fan, javoblar, tarif) VALUES (?,?,?,?)",
            parameters=(file_id, fan, javoblar, tarif),
            commit=True,
        )

    def delete_test(self, id):
        self.execute(
            sql="DELETE FROM Testlar WHERE id = ?", parameters=(id,), commit=True
        )

    def select_test(self, id):
        return self.execute(
            sql="SELECT * FROM Testlar WHERE id = ?", parameters=(id,), fetchone=True
        )

    def select_test_by_fan(self, fan):
        return self.execute(
            sql="SELECT * FROM Testlar WHERE fan = ?", parameters=(fan,), fetchall=True
        )

    def count_tests(self):
        return self.execute("SELECT COUNT(*) FROM Testlar", fetchone=True)

    # Results

    def add_result(self, user_id, test_id, bal, fan_id):
        self.execute(
            sql="INSERT INTO Results(user_id, test_id, bal, fan_id) VALUES(?,?,?,?)",
            parameters=(user_id, test_id, bal, fan_id),
            commit=True,
        )

    def select_result(self, user_id, test_id):
        return self.execute(
            sql="SELECT * FROM Results WHERE user_id = ? AND test_id = ?",
            parameters=(user_id, test_id),
            fetchone=True,
        )

    def count_results(self):
        return self.execute("SELECT COUNT(*) FROM Results", fetchone=True)

    def select_result_fan_id(self, user_id, fan_id):
        return self.execute(
            sql="SELECT * FROM Results WHERE user_id = ? AND fan_id = ?",
            parameters=(user_id, fan_id),
            fetchall=True,
        )

    # Fanlar

    def add_fan(self, nomi, tur):
        self.execute(
            sql="INSERT INTO Fanlar(nomi, tur) VALUES (?,?)",
            parameters=(nomi, tur),
            commit=True,
        )

    def delete_fan(self, id):
        self.execute(
            sql="DELETE FROM Fanlar WHERE id = ?", parameters=(id,), commit=True
        )

    def select_fanlar_by_turi(self, tur):
        return self.execute(
            sql="SELECT * FROM Fanlar WHERE tur = ?", parameters=(tur,), fetchall=True
        )

    def select_fan(self, id):
        return self.execute(
            sql="SELECT * FROM Fanlar WHERE id = ?", parameters=(id,), fetchone=True
        )

    # Temp

    def add_temp(self, id, datetime, test_id, fan_id, status):
        self.execute(
            sql="INSERT INTO Temp(id, datetime, test_id, fan_id, status) VALUES (?,?,?,?,?)",
            parameters=(id, datetime, test_id, fan_id, status),
            commit=True,
        )

    def select_temp(self, id):
        return self.execute(
            sql="SELECT * FROM Temp WHERE id = ?", parameters=(id,), fetchone=True
        )

    def delete_temp(self, id):
        self.execute(sql="DELETE FROM Temp WHERE id = ?", parameters=(id,), commit=True)
