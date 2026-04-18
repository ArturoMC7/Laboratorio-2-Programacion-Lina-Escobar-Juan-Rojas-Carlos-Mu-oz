# Importamos json para archivos, csv para exportar a Excel, y datetime/timedelta para manejar fechas
import json
import csv
from datetime import datetime, timedelta

# --- FUNCIONES DE LECTURA Y ESCRITURA DE LA BASE DE DATOS (db.json) ---
def load_db():
    try:
        # Abrimos el archivo de contratos en modo lectura
        with open('db.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Si no existe, creamos la estructura básica con una lista de contratos vacía
        return {"contracts": []}

def save_db(data):
    # Abrimos el archivo en modo escritura y guardamos los datos con sangría de 4 espacios
    with open('db.json', 'w') as f:
        json.dump(data, f, indent=4)

# --- FUNCIÓN PARA REGISTRAR UN CONTRATO NUEVO ---
def registerContract(number, contractor, obj, start, end, value, supervisor, status, email):
    db = load_db() # Cargamos los contratos actuales
    
    # 1. Validar que el número de contrato no esté repetido
    for c in db['contracts']:
        if c['number'] == number:
            return "number already exists"

    # 2. Validar las fechas
    try:
        # Convertimos los textos de las fechas a un objeto de tiempo real de Python usando el formato Día/Mes/Año
        d_start = datetime.strptime(start, "%d/%m/%Y")
        d_end = datetime.strptime(end, "%d/%m/%Y")
        # Si la fecha de inicio es mayor (más reciente) que la de fin, es un error lógico
        if d_start > d_end:
            return "invalid dates"
    except ValueError:
        # Si el usuario manda una fecha con letras o mal escrita, el strptime falla y capturamos el error aquí
        return "invalid date format"

    # 3. Validar el valor del contrato
    try:
        # Convertimos el valor (que llega como texto) a número decimal (float)
        val_float = float(value)
        # El contrato no puede valer cero o ser negativo
        if val_float <= 0:
            return "invalid value"
    except ValueError:
        # Si mandaron letras en vez de números para el valor
        return "invalid value"

    # 4. Validar el correo electrónico (forma muy básica, solo viendo que tenga @ y un punto)
    if "@" not in email or "." not in email:
        return "invalid email"
    
    # 5. Si pasó todas las pruebas, armamos el diccionario del nuevo contrato
    new_contract = {
        "number": number,
        "contractor": contractor,
        "object": obj,
        "start": start,
        "end": end,
        "value": val_float,
        "supervisor": supervisor,
        "status": status,
        "email": email,
        "trackings": [] # Inicia con una lista de seguimientos vacía
    }
    # Añadimos el contrato y guardamos
    db['contracts'].append(new_contract)
    save_db(db)
    return "ok"

# --- FUNCIÓN PARA LISTAR TODOS LOS CONTRATOS ---
def listContracts():
    db = load_db()
    # Usamos la función sorted de Python. El 'key=lambda...' le dice a Python: "Ordena esta lista basándote en la propiedad 'contractor' (nombre del contratista)"
    return sorted(db['contracts'], key=lambda x: x.get('contractor', ''))

# --- FUNCIÓN PARA BUSCAR UN CONTRATO ESPECÍFICO ---
def searchContract(number):
    db = load_db()
    # Recorremos los contratos y si encontramos el número que nos piden, lo devolvemos
    for c in db['contracts']:
        if c['number'] == number:
            return c
    return None

# --- FUNCIÓN PARA AGREGAR UN SEGUIMIENTO A UN CONTRATO ---
def addTracking(number, date, desc, progress, obs):
    db = load_db()
    
    # Validamos que el avance (progress) sea un número entre 0 y 100
    try:
        prog_float = float(progress)
        if prog_float < 0 or prog_float > 100:
            return "invalid progress"
    except ValueError:
        return "invalid progress"

    # Buscamos a qué contrato le vamos a meter este seguimiento
    for c in db['contracts']:
        if c['number'] == number:
            # Armamos el seguimiento
            new_track = {
                # El ID es automático: miramos cuántos seguimientos hay y le sumamos 1
                "id": len(c['trackings']) + 1,
                "date": date,
                "desc": desc,
                "progress": prog_float,
                "obs": obs
            }
            # Lo metemos en la lista de seguimientos de ESTE contrato específico
            c['trackings'].append(new_track)
            save_db(db)
            return "ok"
            
    # Si recorrió todo y no encontró el contrato
    return "contract not found"

# --- FUNCIÓN PARA LISTAR LOS SEGUIMIENTOS DE UN CONTRATO ---
def listTrackings(number):
    db = load_db()
    for c in db['contracts']:
        if c['number'] == number:
            # Si encuentra el contrato, solo devuelve su lista de seguimientos
            return c['trackings']
    return "contract not found"

# --- FUNCIÓN PARA CALCULAR EL PROMEDIO DE AVANCE ---
def avgProgress(number):
    db = load_db()
    for c in db['contracts']:
        if c['number'] == number:
            tracks = c['trackings'] # Sacamos los seguimientos
            # Si la lista está vacía (no hay seguimientos), el promedio es 0
            if not tracks:
                return {"avg": 0}
            
            # Sumamos todos los 'progress' usando una técnica llamada "comprensión de listas" o generador
            # Luego lo dividimos por la cantidad total de seguimientos (len)
            promedio = sum(t['progress'] for t in tracks) / len(tracks)
            
            # El servidor nos exige que devolvamos un diccionario con la llave "avg"
            return {"avg": promedio} 
    return "contract not found"

# --- FUNCIÓN PARA GENERAR ESTADÍSTICAS ---
def stats():
    db = load_db()
    contracts = db['contracts']
    # Si no hay ningún contrato guardado, no hay estadísticas que mostrar
    if not contracts:
        return {}

    # Sacamos una lista rápida solo con los valores de dinero de todos los contratos
    valores = [float(c['value']) for c in contracts]
    
    # Calculamos la fecha de hoy, y la fecha de hoy más 30 días (para saber cuáles vencen pronto)
    hoy = datetime.now()
    en_un_mes = hoy + timedelta(days=30)

    # Preparamos el diccionario de respuestas
    estadis = {
        "total_by_status": {}, # Para contar cuántos hay ACTIVOS, SUSPENDIDOS, etc.
        "total_value": sum(valores), # Suma total de dinero
        "avg_value": sum(valores) / len(valores), # Dinero total dividido la cantidad de contratos
        "near_expiry": [] # Lista de números de contrato por vencer
    }

    # Recorremos cada contrato para llenar los datos que nos faltan
    for c in contracts:
        estado = c['status']
        # Esto suma 1 al contador del estado correspondiente. Si el estado no existía en el diccionario, empieza en 0 y le suma 1.
        estadis["total_by_status"][estado] = estadis["total_by_status"].get(estado, 0) + 1
        
        # Validamos si vence pronto
        try:
            fecha_fin = datetime.strptime(c['end'], "%d/%m/%Y")
            # Si la fecha de finalización está entre el día de hoy y dentro de 30 días...
            if hoy <= fecha_fin <= en_un_mes:
                # Lo agregamos a la lista de "próximos a vencer"
                estadis["near_expiry"].append(c['number'])
        except:
            # Si hay un error con la fecha, simplemente lo ignoramos (pass) y seguimos con el próximo contrato
            pass

    return estadis

# --- FUNCIÓN PARA EXPORTAR A EXCEL (CSV) ---
def exportCsv():
    db = load_db()
    
    # 1. Crear el CSV de contratos
    # Abrimos (o creamos) contracts.csv en modo escritura. newline='' evita que queden filas vacías de por medio en Windows.
    with open('contracts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f) # Creamos el "escritor" de CSV
        # Escribimos la primera fila, que son los títulos de las columnas
        writer.writerow(['numero', 'contratista', 'estado', 'valor'])
        # Recorremos los contratos y escribimos una fila por cada uno
        for c in db['contracts']:
            writer.writerow([c['number'], c.get('contractor',''), c.get('status',''), c.get('value','')])

    # 2. Crear el CSV de seguimientos (misma lógica)
    with open('trackings.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['numero_contrato', 'fecha', 'avance', 'descripcion', 'observacion'])
        for c in db['contracts']:
            for t in c['trackings']: # Tenemos que hacer un doble ciclo: recorrer contratos, y por cada contrato recorrer sus seguimientos
                writer.writerow([c['number'], t.get('date',''), t.get('progress',''), t.get('desc',''), t.get('obs', '')])

    return True