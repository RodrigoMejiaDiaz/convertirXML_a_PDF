import os
import sys
import time
import shutil

def main():
    if len(sys.argv) != 3:
        print("Uso: updater.exe <ruta_actual> <ruta_nueva>")
        sys.exit(1)
    
    ruta_actual = sys.argv[1]
    ruta_nueva = sys.argv[2]
    
    # Esperar unos segundos para asegurarse de que el programa principal se haya cerrado
    time.sleep(2)
    
    try:
        # Reemplazar el archivo antiguo por el nuevo
        if os.path.exists(ruta_actual):
            shutil.move(ruta_nueva, ruta_actual)  # Reemplaza el archivo
            print("Actualización completada.")
            
            # Opcional: Reiniciar el programa principal
            os.startfile(ruta_actual)
        else:
            print(f"Error: {ruta_actual} no se encuentra.")
            sys.exit(1)

    except Exception as e:
        print(f"Error al actualizar: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
