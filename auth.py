# Importamos la librería json que viene incluida en Python para poder leer y guardar archivos .json
import json

# --- FUNCIÓN PARA LEER EL ARCHIVO DE USUARIOS ---
def load_users():
    # El bloque try-except intenta hacer algo, y si falla (por ejemplo, si el archivo no existe), hace otra cosa sin que el programa se caiga
    try:
        # Abrimos el archivo 'users.json' en modo lectura ('r' de read). La 'f' es el apodo que le damos al archivo abierto
        with open('users.json', 'r') as f:
            # Convertimos el texto del JSON a un diccionario de Python y lo devolvemos
            return json.load(f)
    except FileNotFoundError:
        # Si el archivo no existe (error FileNotFoundError), devolvemos un diccionario con una lista vacía por defecto
        return {"users": []}

# --- FUNCIÓN PARA GUARDAR EN EL ARCHIVO DE USUARIOS ---
def save_users(data):
    # Abrimos el archivo en modo escritura ('w' de write). Esto sobrescribe el archivo con los datos nuevos
    with open('users.json', 'w') as f:
        # Guardamos el diccionario 'data' en el archivo 'f'. indent=4 es para que se guarde ordenado y bonito, no en una sola línea
        json.dump(data, f, indent=4)

# --- FUNCIÓN PARA BUSCAR UN USUARIO ESPECÍFICO ---
def findUser(user):
    data = load_users() # Traemos todos los usuarios del archivo
    # Recorremos la lista de usuarios uno por uno. 'u' representa a cada usuario en la vuelta del ciclo
    for u in data['users']:
        # Si el nombre del usuario 'u' es igual al que estamos buscando...
        if u['user'] == user:
            return u # Devolvemos toda la información de ese usuario
    # Si termina el ciclo y no encontró a nadie, devuelve None (nada)
    return None

# --- FUNCIÓN PARA REGISTRAR UN NUEVO USUARIO ---
def registerUser(user, password, role):
    data = load_users() # Traemos todos los usuarios
    
    # Primero verificamos si el usuario ya existe para no tener duplicados
    for u in data['users']:
        if u['user'] == user:
            # Si ya existe, el servidor espera exactamente esta frase de error
            return "user exists" 
    
    # Si no existe, creamos un nuevo diccionario con sus datos
    new_user = {
        "user": user,
        "password": password,
        "role": role,
        "session": False # Por defecto, cuando se registra, su sesión está apagada
    }
    # Añadimos el nuevo usuario a la lista de usuarios
    data['users'].append(new_user)
    # Guardamos los cambios en el archivo físico
    save_users(data)
    # Le decimos al servidor que todo salió bien
    return "ok"

# --- FUNCIÓN PARA INICIAR O CERRAR SESIÓN ---
def openCloseSession(user, password, flag):
    data = load_users() # Traemos los usuarios
    for u in data['users']:
        # Buscamos al usuario por su nombre
        if u['user'] == user:
            # Si lo encontramos, verificamos que la contraseña coincida
            if u['password'] == password:
                # Si coincide, le cambiamos el estado de la sesión (True para abrir, False para cerrar)
                u['session'] = flag
                save_users(data) # Guardamos el cambio en el archivo
                return "ok"
            else:
                # Si la contraseña está mal, devolvemos error
                return "wrong credentials"
    # Si recorrió todo y no encontró al usuario, también devolvemos error
    return "wrong credentials"

#FUNCIÓN PARA VERIFICAR SI UN USUARIO TIENE PERMISO (ROL)
def hasRole(user, roles):
    data = load_users() # Traemos los usuarios
    for u in data['users']:
        if u['user'] == user:
            # Usamos .get('role') para sacar el rol del usuario. Verificamos si ese rol está dentro de la lista 'roles' permitidos
            return u.get('role') in roles
    # Si el usuario no existe, obviamente no tiene el permiso
    return False