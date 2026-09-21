import pymysql

# Configurações de ligação ao servidor antigo
HOST = '172.27.8.12'
USER = 'root'
PASSWORD = 'F1n'  # Insira a senha aqui se definiu alguma, ou deixe vazia
DATABASE = 'gcon'
PORT = 3306

try:
    connection = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        port=PORT,
        charset='utf8'
    )
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(" Ligação bem-sucedida ao banco antigo via Python!")
        print("Tabelas encontradas:")
        for table in tables[:10]:
            print(" -", table[0])
    connection.close()
except Exception as e:
    print(" Erro de ligação:", e)