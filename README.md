# TP8-programacion3
Copa América 2024 - Gestor de Fixture
Este proyecto es una aplicación en Python diseñada para gestionar el fixture de la Copa América 2024. Permite cargar los datos de los equipos y los partidos desde un archivo CSV, actualizar los resultados de los partidos y calcular las posiciones de los equipos en cada grupo.

Requerimientos
Python 3.x
Archivo CSV con el fixture de la Copa América 2024
Archivo CSV con los resultados de los partidos
Instalación
Clona este repositorio en tu máquina local:
bash
Copiar código
git clone https://github.com/tu_usuario/copa-america-2024.git
Navega al directorio del proyecto:
bash
Copiar código
cd copa-america-2024
Asegúrate de tener los archivos CSV del fixture y los resultados en el directorio del proyecto.
Uso
Ejecuta el script main.py para calcular las posiciones de los equipos:
css
Copiar código
python main.py
El script leerá automáticamente los archivos fixture.csv y resultados.csv en el directorio del proyecto y generará un archivo posiciones.csv con las posiciones de los equipos en cada grupo.
Formato de Archivo CSV
El archivo CSV del fixture debe contener la siguiente estructura:

mathematica
Copiar código
Match Number,Round Number,Date,Location,Home Team,Away Team,Group,Result
El archivo CSV de los resultados debe contener la siguiente estructura:

javascript
Copiar código
Match Number,Home Team Goals,Away Team Goals
Contribuciones
Las contribuciones son bienvenidas. Si encuentras un error o tienes una idea para mejorar el proyecto, por favor abre un problema o envía una solicitud de extracción.