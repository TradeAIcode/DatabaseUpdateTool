import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem

def cargar_archivo(ruta_archivo):
    if ruta_archivo.endswith('.csv'):
        df = pd.read_csv(ruta_archivo)
    elif ruta_archivo.endswith('.xlsx'):
        df = pd.read_excel(ruta_archivo)
    else:
        raise ValueError("Formato de archivo no soportado")
    return df

def mostrar_dataframe_en_tabla(df, tabla):
    tabla.clear()
    tabla.setRowCount(df.shape[0])
    tabla.setColumnCount(df.shape[1])
    tabla.setHorizontalHeaderLabels(df.columns)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            item = QTableWidgetItem(str(df.iat[i, j]))
            tabla.setItem(i, j, item)

    tabla.resizeColumnsToContents()

def actualizar_combobox_con_columnas(df, combobox):
    combobox.clear()
    combobox.addItems(df.columns)