import sqlite3

# Crear una conexión con la base de datos
conn = sqlite3.connect("scores.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                  (name TEXT, score INTEGER)''')

# Obtener la lista de puntajes
def get_scores():
    cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 5")
    return cursor.fetchall()

# Guardar un puntaje en la base de datos
def save_score(name, score):
    cursor.execute("INSERT INTO scores VALUES (?, ?)", (name, score))
    conn.commit()

# Cerrar la conexión con la base de datos
def close_connection():
    cursor.close()
    conn.close()