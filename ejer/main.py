import tkinter as tk
from tkinter import ttk
import csv
import os

class Equipo:
    def __init__(self, nombre, grupo):
        self.nombre = nombre
        self.grupo = grupo
        self.puntos = 0
        self.partidos_jugados = 0
        self.victorias = 0
        self.empates = 0
        self.derrotas = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
        self.diferencia_de_goles = 0

class Partido:
    def __init__(self, numero, ronda, fecha, ubicacion, local, visitante, grupo, goles_local=None, goles_visitante=None):
        self.numero = numero
        self.ronda = ronda
        self.fecha = fecha
        self.ubicacion = ubicacion
        self.local = local
        self.visitante = visitante
        self.grupo = grupo
        self.goles_local = goles_local
        self.goles_visitante = goles_visitante

def leer_fixture_y_resultados(archivo):
    if not os.path.isfile(archivo):
        raise FileNotFoundError(f"El archivo {archivo} no se encontró.")

    partidos = []
    with open(archivo, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            resultado = row['Result'].split('-') if row['Result'] else [None, None]
            goles_local = int(resultado[0]) if resultado[0] else None
            goles_visitante = int(resultado[1]) if resultado[1] else None

            try:
                ronda = int(row['Round Number'])
            except ValueError:
                ronda = row['Round Number']

            partido = Partido(
                int(row['Match Number']),
                ronda,
                row['Date'],
                row['Location'],
                row['Home Team'],
                row['Away Team'],
                row['Group'],
                goles_local,
                goles_visitante
            )
            partidos.append(partido)

    return partidos

def calcular_posiciones(partidos):
    equipos = {}
    for partido in partidos:
        if partido.goles_local is None or partido.goles_visitante is None:
            continue

        local = partido.local
        visitante = partido.visitante
        grupo = partido.grupo
        goles_local = partido.goles_local
        goles_visitante = partido.goles_visitante

        if local not in equipos:
            equipos[local] = Equipo(local, grupo)
        if visitante not in equipos:
            equipos[visitante] = Equipo(visitante, grupo)

        equipos[local].partidos_jugados += 1
        equipos[visitante].partidos_jugados += 1
        equipos[local].goles_a_favor += goles_local
        equipos[local].goles_en_contra += goles_visitante
        equipos[visitante].goles_a_favor += goles_visitante
        equipos[visitante].goles_en_contra += goles_local

        if goles_local > goles_visitante:
            equipos[local].victorias += 1
            equipos[local].puntos += 3
            equipos[visitante].derrotas += 1
        elif goles_local < goles_visitante:
            equipos[visitante].victorias += 1
            equipos[visitante].puntos += 3
            equipos[local].derrotas += 1
        else:
            equipos[local].empates += 1
            equipos[visitante].empates += 1
            equipos[local].puntos += 1
            equipos[visitante].puntos += 1

    for equipo in equipos.values():
        equipo.diferencia_de_goles = equipo.goles_a_favor - equipo.goles_en_contra

    grupos = {}
    for equipo in equipos.values():
        if equipo.grupo not in grupos:
            grupos[equipo.grupo] = []
        grupos[equipo.grupo].append(equipo)

    for grupo in grupos.values():
        grupo.sort(key=lambda x: (x.puntos, x.diferencia_de_goles, x.goles_a_favor), reverse=True)

    return grupos

def generar_informe(grupos, archivo_salida):
    with open(archivo_salida, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Grupo", "Equipo", "Puntos", "PartidosJugados", "Victorias", "Empates", "Derrotas", "GolesAFavor", "GolesEnContra", "DiferenciaDeGoles"])
        for grupo, equipos in grupos.items():
            for equipo in equipos:
                writer.writerow([grupo, equipo.nombre, equipo.puntos, equipo.partidos_jugados, equipo.victorias, equipo.empates, equipo.derrotas, equipo.goles_a_favor, equipo.goles_en_contra, equipo.diferencia_de_goles])

def ingresar_resultados():
    resultados = []

    def guardar_resultado():
        numero = int(entry_numero.get())
        ronda = int(entry_ronda.get())
        fecha = entry_fecha.get()
        ubicacion = entry_ubicacion.get()
        local = entry_local.get()
        visitante = entry_visitante.get()
        grupo = entry_grupo.get()
        goles_local = int(entry_goles_local.get())
        goles_visitante = int(entry_goles_visitante.get())

        partido = Partido(numero, ronda, fecha, ubicacion, local, visitante, grupo, goles_local, goles_visitante)
        resultados.append(partido)

        for entry in [entry_numero, entry_ronda, entry_fecha, entry_ubicacion, entry_local, entry_visitante, entry_grupo, entry_goles_local, entry_goles_visitante]:
            entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Ingreso de Resultados")

    tk.Label(root, text="Número de Partido").grid(row=0, column=0)
    entry_numero = tk.Entry(root)
    entry_numero.grid(row=0, column=1)

    tk.Label(root, text="Ronda").grid(row=1, column=0)
    entry_ronda = tk.Entry(root)
    entry_ronda.grid(row=1, column=1)

    tk.Label(root, text="Fecha").grid(row=2, column=0)
    entry_fecha = tk.Entry(root)
    entry_fecha.grid(row=2, column=1)

    tk.Label(root, text="Ubicación").grid(row=3, column=0)
    entry_ubicacion = tk.Entry(root)
    entry_ubicacion.grid(row=3, column=1)

    tk.Label(root, text="Equipo Local").grid(row=4, column=0)
    entry_local = tk.Entry(root)
    entry_local.grid(row=4, column=1)

    tk.Label(root, text="Equipo Visitante").grid(row=5, column=0)
    entry_visitante = tk.Entry(root)
    entry_visitante.grid(row=5, column=1)

    tk.Label(root, text="Grupo").grid(row=6, column=0)
    entry_grupo = tk.Entry(root)
    entry_grupo.grid(row=6, column=1)

    tk.Label(root, text="Goles Local").grid(row=7, column=0)
    entry_goles_local = tk.Entry(root)
    entry_goles_local.grid(row=7, column=1)

    tk.Label(root, text="Goles Visitante").grid(row=8, column=0)
    entry_goles_visitante = tk.Entry(root)
    entry_goles_visitante.grid(row=8, column=1)

    tk.Button(root, text="Guardar Resultado", command=guardar_resultado).grid(row=9, column=0, columnspan=2)

    root.mainloop()

    return resultados

if __name__ == "__main__":
    while True:
        print("\n--- Menú ---")
        print("1. Leer archivo de resultados")
        print("2. Calcular posiciones")
        print("3. Generar informe")
        print("4. Ingresar resultados manualmente")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            archivo_resultados = input("Ingrese el nombre del archivo de resultados: ")
            try:
                partidos = leer_fixture_y_resultados(archivo_resultados)
                print("Archivo leído correctamente.")
            except FileNotFoundError as e:
                print(e)
            except KeyError as e:
                print(f"Error en el archivo CSV: {e}")
            except ValueError as e:
                print(f"Error de valor: {e}")
        
        elif opcion == '2':
            try:
                grupos = calcular_posiciones(partidos)
                print("Posiciones calculadas correctamente.")
            except NameError:
                print("Primero debe leer el archivo de resultados o ingresar resultados manualmente.")
        
        elif opcion == '3':
            archivo_salida = input("Ingrese el nombre del archivo de salida: ")
            try:
                generar_informe(grupos, archivo_salida)
                print(f"Informe generado correctamente en '{archivo_salida}'.")
            except NameError:
                print("Primero debe calcular las posiciones.")
        
        elif opcion == '4':
            try:
                partidos = ingresar_resultados()
                print("Resultados ingresados correctamente.")
            except Exception as e:
                print(f"Error al ingresar resultados: {e}")

        elif opcion == '5':
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")
