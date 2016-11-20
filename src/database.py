import mysql.connector


def connect():
    return mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        database='buenosaires_TPT')

def get_prenoms(lower_case=False):
    cnt = connect()
    cursor = cnt.cursor()

    query = "SELECT DISTINCT prenom FROM prenom"
    cursor.execute(query)
    if lower_case:
        prenoms = [row[0].lower() for row in cursor]
    else:
        prenoms = [row[0] for row in cursor]

    cursor.close()
    cnt.close()
    return prenoms

def get_noms(lower_case=False):
    cnt = connect()
    cursor = cnt.cursor()

    query = "SELECT DISTINCT nom FROM nom"
    cursor.execute(query)
    if lower_case:
        noms = [row[0].lower() for row in cursor]
    else:
        noms = [row[0] for row in cursor]

    cursor.close()
    cnt.close()
    return noms;
