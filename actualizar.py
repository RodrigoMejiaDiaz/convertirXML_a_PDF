import requests
from dotenv import dotenv_values
import os
import sys
import subprocess

def cargar_env():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    dotenv_path = os.path.join(base_path, ".env")
    return dotenv_values(dotenv_path)

def obtener_version_actual_txt():
    version_path = os.path.join(os.path.dirname(__file__), "version.txt")
    with open(version_path, "r") as file:
        return file.read().strip()

def obtener_ultima_version(repo, version_actual):
    secrets = cargar_env()
    headers = {"Authorization": f"token {secrets['TOKEN']}"}
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        release_data = response.json()
        ultima_version = release_data["tag_name"]
        if ultima_version != version_actual:
            print(release_data["assets"][0]["url"])                        
            return release_data["assets"][0]["url"], ultima_version
    return None, None

def descargar_archivo(url, destino):
    secrets = cargar_env()
    
    # Configuración de los headers con el token de GitHub
    headers = {
        "Authorization": f"Bearer {secrets['TOKEN']}",
        "Accept": "application/octet-stream",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Realizar la petición GET con los headers
    response = requests.get(url, headers=headers, stream=True)
    
    print(f"Status Code: {response.status_code}")  # Imprime el código de estado para ver si es 200 o 404
    
    if response.status_code == 200:
        with open(destino, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Archivo descargado correctamente a {destino}")
    else:
        print(f"Error al descargar el archivo: {response.status_code}")
        print(f"Respuesta: {response.text}")  # Imprimir el mensaje de error

def actualizar_programa(url_actualizacion):
    # Ruta del nuevo archivo descargado
    nuevo_ejecutable = os.path.join(os.path.dirname(sys.executable), "nuevo_programa.exe")
    descargar_archivo(url_actualizacion, nuevo_ejecutable)
    
    # Ruta del actualizador
    updater_path = os.path.join(os.path.dirname(sys.executable), "updater.exe")
    
    # Ejecutar el actualizador y salir
    subprocess.Popen([updater_path, sys.executable, nuevo_ejecutable])
    sys.exit(0)