import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self._connection = None

    def get_connection(self):
        """Get a connection to the SQLite database"""
        if self._connection is None:
            self._connection = sqlite3.connect(
                self.db_path, detect_types=sqlite3.PARSE_DECLTYPES
            )
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def close_connection(self):
        """Close the database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def get_films_by_month(self, month_digit):
        """Get films filtered by month"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM films 
            WHERE strftime('%m', release_date) = ?
        """,
            (month_digit,),
        )

        films = [dict(row) for row in cursor.fetchall()]
        return films

    def get_albums_by_month(self, month_digit):
        """Get albums filtered by month"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM albums 
            WHERE strftime('%m', release_date) = ?
        """,
            (month_digit,),
        )

        albums = [dict(row) for row in cursor.fetchall()]
        return albums

    def get_books_by_month(self, month_digit):
        """Get books filtered by month"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM books 
            WHERE strftime('%m', release_date) = ?
        """,
            (month_digit,),
        )

        books = [dict(row) for row in cursor.fetchall()]
        return books

    def get_authors_by_birth_month(self, month_digit):
        """Get authors filtered by birth month"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM authors 
            WHERE strftime('%m', birth) = ?
        """,
            (month_digit,),
        )

        authors = [dict(row) for row in cursor.fetchall()]
        return authors

    def get_authors_by_death_month(self, month_digit):
        """Get authors filtered by death month"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM authors 
            WHERE strftime('%m', death) = ? AND death IS NOT NULL
        """,
            (month_digit,),
        )

        authors = [dict(row) for row in cursor.fetchall()]
        return authors

    def get_random_fact(self):
        """Get a random fact from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT fact FROM facts ORDER BY RANDOM() LIMIT 1")
        fact = cursor.fetchone()[0]

        return fact

    # Legacy methods for compatibility
    def get_films(self):
        """Get all films from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM films")
        films = [dict(row) for row in cursor.fetchall()]

        return films

    def get_albums(self):
        """Get all albums from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM albums")
        albums = [dict(row) for row in cursor.fetchall()]

        return albums

    def get_books(self):
        """Get all books from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")
        books = [dict(row) for row in cursor.fetchall()]

        return books

    def get_authors(self):
        """Get all authors from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors")
        authors = [dict(row) for row in cursor.fetchall()]

        return authors
