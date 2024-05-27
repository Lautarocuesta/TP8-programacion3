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

    print("Leyendo archivo:", archivo)

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

    print("Se han leído", len(partidos), "partidos.")

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

if __name__ == "__main__":
    archivo_resultados = "resultados.csv"

    try:
        partidos = leer_fixture_y_resultados(archivo_resultados)
        grupos = calcular_posiciones(partidos)
        generar_informe(grupos, "posiciones.csv")
        print("El informe se ha generado correctamente en 'posiciones.csv'.")
    except FileNotFoundError as e:
        print(e)
    except KeyError as e:
        print(f"Error en el archivo CSV: {e}")
    except ValueError as e:
        print(f"Error de valor: {e}")
