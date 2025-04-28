import pandas as pd
import mysql.connector
import pyodbc

def conectar_y_leer_tabla(host, usuario, contraseña, base_datos, tabla, puerto=3306, tipo_bd="MySQL"):
    if tipo_bd == "MySQL":
        conn = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contraseña,
            database=base_datos,
            port=puerto
        )
        query = f"SELECT * FROM {tabla}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    elif tipo_bd == "SQL Server":
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={host},{puerto};"
            f"DATABASE={base_datos};"
            f"UID={usuario};"
            f"PWD={contraseña};"
            f"Encrypt=no;"
        )
        query = f"SELECT * FROM {tabla}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    else:
        raise ValueError("Tipo de base de datos no soportado: " + tipo_bd)

def exportar_dataframe(df, ruta_salida):
    if ruta_salida.endswith('.csv'):
        df.to_csv(ruta_salida, index=False)
    elif ruta_salida.endswith('.xlsx'):
        df.to_excel(ruta_salida, index=False)
    else:
        raise ValueError("Extensión de archivo no soportada (.csv o .xlsx)")