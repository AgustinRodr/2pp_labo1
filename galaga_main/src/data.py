import sqlite3

# Crear una conexion con la base de datos
try:
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    # Crear la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                      (name TEXT, score INTEGER)''')
except sqlite3.Error as e:
    print("Error al conectar a la base de datos:", e)

# Obtener la lista de puntajes
def get_scores():
    try:
        cursor.execute("SELECT DISTINCT name, MAX(score) FROM scores GROUP BY name ORDER BY score DESC LIMIT 5")
        return cursor.fetchall()

    except sqlite3.Error as e:
        print("Error al obtener los puntajes:", e)

# Guardar un puntaje en la base de datos
def save_score(name, score):
    try:
        cursor.execute("INSERT INTO scores VALUES (?, ?)", (name, score))
        conn.commit()

    except sqlite3.Error as e:
        print("Error al guardar el puntaje:", e)

# Cerrar la conexión con la base de datos
def close_connection():
    try:
        cursor.close()
        conn.close()

    except sqlite3.Error as e:
        print("Error al cerrar la conexión:", e)