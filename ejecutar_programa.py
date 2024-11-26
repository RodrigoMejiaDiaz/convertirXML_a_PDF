from tkinter import Tk
from main import Xml_a_pdf  # Asegúrate de que '' es el nombre del archivo de tu clase

def start_program():
    root = Tk()
    Xml_a_pdf(root)
    root.mainloop()

if __name__ == "__main__":
    start_program()