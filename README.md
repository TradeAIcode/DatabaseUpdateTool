# 🛠️ Actualizador de Base de Datos

[![Python](https://img.shields.io/badge/Python-3.9-blue)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

# 📚 Tabla de Contenidos
- [Descripción](#-descripción)
- [Vista previa](#-vista-previa-de-la-aplicación)
- [Características](#-características-principales)
- [Instalación y requisitos](#-instalación-y-requisitos)
- [Uso detallado](#-uso-detallado)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Licencia](#-licencia)

---

## 📚 Descripción

**Actualizador de Base de Datos** es una potente herramienta en Python que permite actualizar registros de tablas de forma automática, fácil y segura:

- Carga un archivo antiguo para modificar.
- Carga un archivo nuevo con datos actualizados.
- Actualiza campos automáticamente según claves.
- Exporta tablas completas de base de datos a CSV o Excel.
- Soporta conexiones a **MySQL** y **SQL Server**.

Ideal para automatizar tareas de mantenimiento de bases de datos.

---

## 📸 Vista previa de la aplicación

*(Pronto: insertar captura de pantalla del GUI PyQt5)*

---

## ✨ Características principales

- Interfaz gráfica moderna con **PyQt5**.
- Ordenar cualquier columna con solo hacer clic en la cabecera.
- Logs de actividad informativos en cada pestaña.
- Actualización de campos inteligente (solo si cambian y no están vacíos).
- Exportación rápida de datos a **CSV** y **Excel**.
- Configuración persistente usando `config.json`.
- Soporte para dos tipos de bases de datos: **MySQL** y **SQL Server**.
- Cálculo y visualización de número de registros.

---

## ⚙️ Instalación y requisitos

### Requisitos

- Python 3.8 o superior
- PyQt5
- pandas
- openpyxl
- pyodbc
- pymysql

Instalación rápida:

```bash
pip install -r requirements.txt
```

**Notas adicionales:**
- Para conexiones SQL Server debes tener instalado un driver ODBC compatible.
- Para conexiones MySQL debes asegurarte que `pymysql` esté disponible.

---

## 🚀 Uso detallado

### Configuración inicial

1. Abre la aplicación.
2. Dirígete a la pestaña **"Configuración (Base de Datos)"**.
3. Introduce:
   - Servidor
   - Puerto
   - Usuario
   - Contraseña
   - Nombre de la base de datos
   - Nombre de la tabla
   - Tipo de base de datos (MySQL o SQL Server)
4. Haz clic en **"Guardar Configuración"**.

### Operaciones en la Base de Datos

- Puedes hacer clic en **"Leer y Mostrar Tabla"** para ver una vista previa de la tabla.
- Luego puedes exportar la tabla directamente a un archivo CSV o Excel.

### Actualizar Datos desde Archivos

1. Ve a la pestaña **"Principal (Actualizar Datos)"**.
2. Carga el **archivo a modificar**.
3. Carga el **archivo con los datos nuevos**.
4. Selecciona:
   - El campo a actualizar
   - El campo clave (para emparejar registros)
5. Haz clic en **"Actualizar Datos"**.
6. Revisa los cambios en la vista previa.
7. Exporta el archivo actualizado si lo deseas.

---

## 💪 Tecnologías utilizadas

- [Python](https://www.python.org/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
- [pyodbc](https://github.com/mkleehammer/pyodbc)
- [pymysql](https://pymysql.readthedocs.io/en/latest/)

---

## 📄 Licencia

Este proyecto está licenciado bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

> Desarrollado con ❤️ por 

