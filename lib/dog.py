import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        return cls(name=row[1], breed=row[2], id=row[0])

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name = ? LIMIT 1", (name,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM dogs WHERE id = ? LIMIT 1", (id,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        CURSOR.execute("SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1", (name, breed))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return cls.create(name, breed)

    def update(self):
        CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))
        CONN.commit()
