from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QComboBox,
    QFileDialog, QMessageBox, QFrame, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from file_utils import cargar_archivo, mostrar_dataframe_en_tabla, actualizar_combobox_con_columnas
from db_utils import conectar_y_leer_tabla, exportar_dataframe
import pandas as pd
import json
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actualizador de Base de Datos - TradeAIcode")
        self.resize(1200, 800)
        
        self.df_old = None
        self.df_new = None
        self.config_file = "config.json"
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.tab_principal = QWidget()
        self.tab_config = QWidget()
        
        self.tabs.addTab(self.tab_principal, "Principal (Actualizar Datos)")
        self.tabs.addTab(self.tab_config, "Configuración (Base de Datos)")
        
        self.init_tab_config()
        self.init_tab_principal()
        
        self.load_config()

    def init_tab_config(self):
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()  # Parte superior: campos + botones
        fields_layout = QVBoxLayout()
        buttons_layout = QVBoxLayout()

        self.db_host = QLineEdit()
        self.db_port = QLineEdit()
        self.db_user = QLineEdit()
        self.db_pass = QLineEdit()
        self.db_name = QLineEdit()
        self.db_table = QLineEdit()
        self.db_type = QComboBox()

        self.db_pass.setEchoMode(QLineEdit.Password)
        self.db_type.addItems(["MySQL", "SQL Server"])

        fields = [
            ("Servidor (localhost):", self.db_host),
            ("Puerto (Manual):", self.db_port),
            ("Usuario:", self.db_user),
            ("Contraseña:", self.db_pass),
            ("Nombre de Base de Datos:", self.db_name),
            ("Nombre de la Tabla:", self.db_table),
            ("Tipo de Base de Datos:", self.db_type),
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            fields_layout.addWidget(label)
            fields_layout.addWidget(widget)

        fields_layout.setSpacing(5)  # Compactar los campos
        fields_layout.setContentsMargins(10, 10, 10, 10)

        self.btn_save_config = QPushButton("Guardar Configuración")
        self.btn_save_config.setMinimumHeight(40)
        self.btn_save_config.setIcon(QIcon("icons/save.png"))
        self.btn_save_config.clicked.connect(self.save_config)

        self.btn_read_db = QPushButton("Leer y Mostrar Tabla")
        self.btn_read_db.setMinimumHeight(40)
        self.btn_read_db.setIcon(QIcon("icons/refresh.png"))
        self.btn_read_db.clicked.connect(self.leer_base_datos)

        self.btn_export_db = QPushButton("Exportar Tabla (CSV/Excel)")
        self.btn_export_db.setMinimumHeight(40)
        self.btn_export_db.setIcon(QIcon("icons/save.png"))
        self.btn_export_db.clicked.connect(self.exportar_tabla_db)

        buttons_layout.addWidget(self.btn_save_config)
        buttons_layout.addWidget(self.btn_read_db)
        buttons_layout.addWidget(self.btn_export_db)
        buttons_layout.addStretch()

        top_layout.addLayout(fields_layout, stretch=3)
        top_layout.addLayout(buttons_layout, stretch=1)

        # Parte inferior: vista previa + log
        self.table_preview_config = QTableWidget()
        self.log_text_config = QTextEdit()
        self.log_text_config.setReadOnly(True)
        self.log_text_config.setMaximumHeight(100)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(QLabel("Vista previa tabla cargada:"))
        main_layout.addWidget(self.table_preview_config)
        main_layout.addWidget(QLabel("Log de conexión:"))
        main_layout.addWidget(self.log_text_config)

        self.tab_config.setLayout(main_layout)



    def init_tab_principal(self):
        main_layout = QVBoxLayout()
        columns_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.btn_load_old = QPushButton("Cargar Archivo a MODIFICAR")
        self.combo_old_field = QComboBox()
        self.combo_old_key = QComboBox()
        self.table_preview_old = QTableWidget()

        self.btn_load_old.clicked.connect(self.cargar_archivo_antiguo)

        left_layout.addWidget(self.btn_load_old)
        left_layout.addWidget(QLabel("Campo a actualizar:"))
        left_layout.addWidget(self.combo_old_field)
        left_layout.addWidget(QLabel("Campo clave:"))
        left_layout.addWidget(self.combo_old_key)
        left_layout.addWidget(QLabel("Vista previa archivo a modificar:"))
        left_layout.addWidget(self.table_preview_old)

        left_frame = QFrame()
        left_frame.setLayout(left_layout)
        left_frame.setFrameShape(QFrame.StyledPanel)
        left_frame.setStyleSheet("background-color: #F0F8FF; border: 1px solid #A9A9A9; border-radius: 5px;")

        right_layout = QVBoxLayout()

        self.btn_load_new = QPushButton("Cargar Archivo Datos para Extraer")
        self.combo_new_field = QComboBox()
        self.combo_new_key = QComboBox()
        self.table_preview_new = QTableWidget()

        self.btn_load_new.clicked.connect(self.cargar_archivo_nuevo)

        right_layout.addWidget(self.btn_load_new)
        right_layout.addWidget(QLabel("Campo a extraer:"))
        right_layout.addWidget(self.combo_new_field)
        right_layout.addWidget(QLabel("Campo clave:"))
        right_layout.addWidget(self.combo_new_key)
        right_layout.addWidget(QLabel("Vista previa archivo Datos para Extraer:"))
        right_layout.addWidget(self.table_preview_new)

        right_frame = QFrame()
        right_frame.setLayout(right_layout)
        right_frame.setFrameShape(QFrame.StyledPanel)
        right_frame.setStyleSheet("background-color: #F5FFFA; border: 1px solid #A9A9A9; border-radius: 5px;")

        columns_layout.addWidget(left_frame)
        columns_layout.addWidget(right_frame)

        main_layout.addLayout(columns_layout)

        # Botón Actualizar Datos
        self.btn_update_data = QPushButton("Actualizar Datos")
        self.btn_update_data.setMinimumHeight(40)
        self.btn_update_data.setIcon(QIcon("icons/refresh.png"))  # Asegúrate de tener este icono
        self.btn_update_data.clicked.connect(self.actualizar_datos)
        main_layout.addWidget(self.btn_update_data, alignment=Qt.AlignCenter)

        # Botón Guardar Archivo Modificado
        self.btn_save_modified = QPushButton("Guardar Archivo Modificado")
        self.btn_save_modified.setMinimumHeight(40)
        self.btn_save_modified.setIcon(QIcon("icons/save.png"))  # Asegúrate de tener este icono
        self.btn_save_modified.clicked.connect(self.guardar_archivo_modificado)
        main_layout.addWidget(self.btn_save_modified, alignment=Qt.AlignCenter)

        # Log de Actividades
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)  # <-- Log más pequeño
        main_layout.addWidget(QLabel("Log de Actividades:"))
        main_layout.addWidget(self.log_text)

        self.tab_principal.setLayout(main_layout)

    def log(self, mensaje, tipo="info"):
        if tipo == "ok":
            color = "green"
            emoji = "✔️ "
        elif tipo == "error":
            color = "red"
            emoji = "❌ "
        else:
            color = "blue"
            emoji = "ℹ️ "
        self.log_text.append(f'<span style="color:{color}">{emoji}{mensaje}</span>')

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self.db_host.setText(config.get("host", ""))
            self.db_port.setText(str(config.get("port", "3306")))
            self.db_user.setText(config.get("user", ""))
            self.db_pass.setText(config.get("password", ""))
            self.db_name.setText(config.get("database", ""))
            self.db_table.setText(config.get("table", ""))
            self.db_type.setCurrentText(config.get("db_type", "MySQL"))
            self.log("Configuración cargada.", "ok")

    def save_config(self):
        config = {
            "host": self.db_host.text(),
            "port": int(self.db_port.text()) if self.db_port.text() else 3306,
            "user": self.db_user.text(),
            "password": self.db_pass.text(),
            "database": self.db_name.text(),
            "table": self.db_table.text(),
            "db_type": self.db_type.currentText()
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        self.log("Configuración guardada.", "ok")
        QMessageBox.information(self, "✔️ Guardado", "✔️ Configuración guardada correctamente.")

    def cargar_archivo_antiguo(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo a Modificar", "", "Archivos CSV/Excel (*.csv *.xlsx)")
        if ruta:
            self.df_old = cargar_archivo(ruta)
            mostrar_dataframe_en_tabla(self.df_old, self.table_preview_old)
            self.table_preview_old.setSortingEnabled(True)  # <-- Añadir aquí
            self.aplicar_estilo_tabla(self.table_preview_old)
            actualizar_combobox_con_columnas(self.df_old, self.combo_old_field)
            actualizar_combobox_con_columnas(self.df_old, self.combo_old_key)
            self.log("Archivo a Modificar cargado.", "ok")

    def cargar_archivo_nuevo(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo Datos para Extraer", "", "Archivos CSV/Excel (*.csv *.xlsx)")
        if ruta:
            self.df_new = cargar_archivo(ruta)
            mostrar_dataframe_en_tabla(self.df_new, self.table_preview_new)
            self.table_preview_new.setSortingEnabled(True)  # <-- Añadir aquí
            self.aplicar_estilo_tabla(self.table_preview_new)
            actualizar_combobox_con_columnas(self.df_new, self.combo_new_field)
            actualizar_combobox_con_columnas(self.df_new, self.combo_new_key)
            self.log("Archivo Datos para Extraer cargado.", "ok")

    def actualizar_datos(self):
        if self.df_old is None or self.df_new is None:
            QMessageBox.warning(self, "⚠️ Advertencia", "⚠️ Debes cargar ambos archivos primero.")
            return

        old_key = self.combo_old_key.currentText()
        new_key = self.combo_new_key.currentText()
        old_field = self.combo_old_field.currentText()
        new_field = self.combo_new_field.currentText()

        if not old_key or not new_key or not old_field or not new_field:
            QMessageBox.warning(self, "⚠️ Advertencia", "⚠️ Debes seleccionar correctamente los campos.")
            return

        new_dict = self.df_new.set_index(new_key)[new_field].to_dict()
        cambios = 0

        for idx, row in self.df_old.iterrows():
            articulo = str(row[old_key]).strip()  # <- Aseguramos que sea string limpio
            nuevo_valor = new_dict.get(articulo)

            if nuevo_valor is not None:
                actual_valor = str(row[old_field]).strip()
                nuevo_valor_str = str(nuevo_valor).strip()
                
                if actual_valor != nuevo_valor_str:
                    self.df_old.at[idx, old_field] = nuevo_valor
                    cambios += 1

        mostrar_dataframe_en_tabla(self.df_old, self.table_preview_old)
        self.log(f"Se actualizaron {cambios} registros.", "ok")
        QMessageBox.information(self, "✔️ Actualización Completa", f"✔️ Se actualizaron {cambios} registros.")


    def guardar_archivo_modificado(self):
        if self.df_old is None:
            QMessageBox.warning(self, "⚠️ Advertencia", "⚠️ No hay datos para guardar.")
            return
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo Modificado", "", "CSV (*.csv);;Excel (*.xlsx)")
        if ruta:
            try:
                exportar_dataframe(self.df_old, ruta)
                self.log(f"Archivo modificado guardado: {ruta}", "ok")
                QMessageBox.information(self, "✔️ Éxito", "✔️ Archivo modificado guardado correctamente.")
            except Exception as e:
                self.log(f"Error al guardar: {str(e)}", "error")
                QMessageBox.critical(self, "❌ Error", f"❌ Error al guardar archivo modificado.")

    
    def leer_base_datos(self):
        try:
            tipo = self.db_type.currentText()
            self.log_text_config.append(f"ℹ️ Leyendo base de datos ({tipo})...")

            df = conectar_y_leer_tabla(
                self.db_host.text(),
                self.db_user.text(),
                self.db_pass.text(),
                self.db_name.text(),
                self.db_table.text(),
                int(self.db_port.text()) if self.db_port.text() else 3306,
                tipo
            )

            # 🔵 Limpiar la tabla ANTES de mostrar la nueva
            self.table_preview_config.clear()
            self.table_preview_config.setRowCount(0)
            self.table_preview_config.setColumnCount(0)
            self.table_preview_config.setHorizontalHeaderLabels([])

            # Mostrar nuevo DataFrame
            mostrar_dataframe_en_tabla(df, self.table_preview_config)
            self.table_preview_config.setSortingEnabled(True)
            self.aplicar_estilo_tabla(self.table_preview_config)

            self.db_preview_df = df

            total_registros = len(df)
            self.log_text_config.append(f"✔️ Tabla de base de datos cargada correctamente. ✅ {total_registros} registros encontrados.")
            QMessageBox.information(self, "✔️ Éxito", f"✔️ Tabla cargada correctamente. {total_registros} registros encontrados.")

        except Exception as e:
            self.log_text_config.append(f"❌ Error: {str(e)}")
            QMessageBox.critical(self, "❌ Error", f"❌ {str(e)}")





    def exportar_tabla_db(self):
        if not hasattr(self, 'db_preview_df') or self.db_preview_df is None:
            QMessageBox.warning(self, "⚠️ Advertencia", "⚠️ Primero debes cargar una tabla desde la base de datos.")
            return

        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "CSV (*.csv);;Excel (*.xlsx)")
        if ruta:
            try:
                exportar_dataframe(self.db_preview_df, ruta)
                self.log_text_config.append(f"✔️ Archivo exportado: {ruta}")
                QMessageBox.information(self, "✔️ Éxito", "✔️ Archivo exportado correctamente.")
            except Exception as e:
                self.log_text_config.append(f"❌ Error al exportar: {str(e)}")
                QMessageBox.critical(self, "❌ Error", f"❌ {str(e)}")
                
    
    def aplicar_estilo_tabla(self, tabla):
        tabla.setStyleSheet("""
            QHeaderView::section {
                background-color: #f0f0f0;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #d0d0d0;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
            }
        """)            