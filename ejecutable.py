## Comprobar actualizaciones
from actualizar import obtener_ultima_version, actualizar_programa, obtener_version_actual_txt
from main import Xml_a_pdf
from tkinter import Tk

def ejecutable():
    repo = "RodrigoMejiaDiaz/convertirXML_a_PDF"
    version_actual = obtener_version_actual_txt()

    print(f"Versión actual: {version_actual}")

    url_actualizacion, ultima_version = obtener_ultima_version(repo, version_actual)
    if url_actualizacion:
        print(f"Nueva versión disponible: {ultima_version}. Actualizando...")
        actualizar_programa(url_actualizacion)
    else:
        print("El programa está actualizado.")
        # Iniciar programa      
        root = Tk()
        Xml_a_pdf(root)
        root.mainloop()

if __name__ == "__main__":
    ejecutable()