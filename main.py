import xml.etree.ElementTree as ET
from pathlib import Path
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
import zipfile
from fillpdf import fillpdfs

class Xml_a_pdf:
    def __init__(self, root):
        self.root = root
        
        self.archivosXML = []
        
        self.errores = []
        
        self.carpeta_destino = ""
        
        self.numerosTexto = {
            '32.00': 'Son: Treinta y dos con 00/100. Soles',
            '30.70': 'Son: Treinta con 70/100. Soles',
            '28.00': 'Son: Veintiocho con 00/100. Soles',
            '26.90': 'Son: Veintiséis con 90/100. Soles',
            '23.10': 'Son: Veintitrés con 10/100. Soles',
            '20.00': 'Son: Veinte con 00/100. Soles',
            '19.20': 'Son: Diesinueve con 20/100. Soles',
            '16.00': 'Son: Dieciséis con 00/100. Soles',
            '15.40': 'Son: Quince con 40/100. Soles',
            '12.00': 'Son: Doce con 00/100. Soles',
            '11.60': 'Son: Once con 60/100. Soles',
            '8.00': 'Son: Ocho con 00/100. Soles',
            '7.70': 'Son: Siete con 70/100. Soles',
            '5.00': 'Son: Cinco con 00/100. Soles',
            '3.90': 'Son: Tres con 90/100. Soles',
            '1.20': 'Son: Uno con 20/100. Soles',
            '0.60': 'Son: Cero con 60/100. Soles'
        }
        
        # Variable para almacenar el progreso de la barra de carga General
        self.progresoGeneral = 0
        
        # Variable para almacenar el total de la barra de carga
        self.total = 0
        
        self.datos_formulario = {}
        
        self.peaje_nombres = {
            '1': 'Matarani',
            '2': 'Uchumayo',
            '3': 'Unidad de Peaje Patahuasi km 78+200 Ruta 30B',
            '4': 'Unidad de Peaje Santa Lucia km 201+700 Ruta 30B',
            '5': 'Illpa',
            '6': 'Unidad de Peaje Pampa Cuellar km 65+000 Ruta 34A',
            '7': 'Ilo'
        }
        
        ## Configuracion TKinter
        
        self.root.title("Convertir XML a PDF")
        self.root.resizable(FALSE, FALSE)
        
        # Especificar el tamaño de la ventana
        ancho_ventana = 350
        alto_ventana = 400

        # Configuración del mainframe
        mainframe = ttk.Frame(self.root, width=ancho_ventana, height=alto_ventana, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        # Añadir los widgets a utilizar y ubicarlos en el grid
        lblArchivoXML = ttk.Label(mainframe, text="Selecciona los archivos XML:", wraplength=100)
        
        self.btnSeleccionarXML = ttk.Button(mainframe, text="Seleccionar XML", command=self.seleccionarCarpeta_o_ArchivosXML)
        
        # Variable para almacenar estado de archivo seleccionado
        self.estaSeleccionadoXML = StringVar()
        self.estaSeleccionadoXML.set("")
        self.lblCargadosXML = ttk.Label(mainframe, textvariable=self.estaSeleccionadoXML, wraplength=100)
        
        # Vincular función para verificar cambios
        self.estaSeleccionadoXML.trace_add("write", self.escuchar_cambios_seleccionado)
        
        self.btnConvertir = ttk.Button(mainframe, text="Convertir", command=self.btnConvertir_handler)
        btnCerrar = ttk.Button(mainframe, text="Cerrar Programa", command=self.cerrarPrograma)
        
        # Configuracion grid
        lblArchivoXML.grid(column=0, row=0)
        self.btnSeleccionarXML.grid(column=1, row=0)
        self.lblCargadosXML.grid(column=2, row=0)
        self.btnConvertir.grid(column=1,row=1)
        btnCerrar.grid(column=1, row=2)
        
        # Cambiar estados a desabilitados
        self.btnConvertir.state(['disabled'])
        
        # Barra de progreso
        self.progreso = ttk.Progressbar(mainframe, orient="horizontal", mode="determinate")
        self.progreso.grid(column=0, row=3, sticky="nswe", columnspan=3)

        # Etiqueta que muestra el progreso en texto
        self.label_progreso = ttk.Label(mainframe, text="Progreso: 0%")
        self.label_progreso.grid(column=1, row=4, sticky="ns")
        
        # Centra ventana al abrir programa
        self.centrar_ventana(self.root, ancho_ventana, alto_ventana)
        
        # Configura el peso del programa padre para que se amplie con la ventana
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Asigna los pesos para que se amplien con la ventana
        mainframe.columnconfigure(0, weight=1, uniform="col")
        mainframe.columnconfigure(1, weight=1, uniform="col")
        mainframe.columnconfigure(2, weight=1, uniform="col")
        
        mainframe.rowconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=1)
        mainframe.rowconfigure(2, weight=1)
        mainframe.rowconfigure(3, weight=1)
        mainframe.rowconfigure(4, weight=1)
        
        # Loop para dar padding a todos los widgets hijos
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
    
    def cerrarPrograma(self):
        self.root.destroy() 
    
    # Función para que la ventana principal (self.root) se abra en el centro de la pantalla
    def centrar_ventana(self, ventana, ancho, alto):
        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        # Calcular las coordenadas x, y para centrar la ventana
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)

        # Fijar las dimensiones y la posición de la ventana
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    # Función para actualizar barra de progreso    
    def actualizar_progresoGeneral(self, total):
        ## Actualizar barra de progreso
        # aumentar en 1 el progreso
        self.progresoGeneral += 1
        
        # Actualizar la barra de progreso
        self.progreso["value"] = self.progresoGeneral  # Actualizar el valor de la barra
        self.label_progreso.config(text=f"Progreso: {int((self.progresoGeneral) / total * 100)}%")

        # Actualizar la interfaz gráfica
        self.root.update_idletasks() 
    
    # Función para reiniciar el progreso de la barra General       
    def reiniciar_progresoGeneral(self):
        self.carpeta_destino = ""
        # Reiniciar la variable de progresoGeneral
        self.progresoGeneral = 0
        # Actualizar la barra de progreso
        self.progreso["value"] = self.progresoGeneral  # Actualizar el valor de la barra
        self.label_progreso.config(text="Progreso: 0%")
    
    # Verificar cambios self.estan_cagados
    def escuchar_cambios_seleccionado(self, *args):
        estaSeleccionadoXML = self.estaSeleccionadoXML.get()
        if estaSeleccionadoXML != "" and estaSeleccionadoXML != "No se seleccionó archivo" :
            self.btnConvertir.state(['!disabled'])
        else:
            self.btnConvertir.state(['disabled'])

    # Función para abrir ventana emergente para seleccionar los archivos
    def seleccionarCarpeta_o_ArchivosXML(self):
        
        # Preguntar al usuario si quiere seleccionar una carpeta o archivos
        opcion = messagebox.askquestion(
            "Seleccionar",
            "¿Deseas seleccionar una carpeta entera?",
            icon="question"
        )
        
        # Seleccionar archivos XML o carpeta según la respuesta del usuario
        if opcion == "yes":  # Si elige 'Sí', selecciona una carpeta
            # Abrir ventana para seleccionar carpeta
            carpeta = filedialog.askdirectory(title="Seleccionar carpeta")
            
            # Comprobar si se ha seleccionado una carpeta
            if carpeta:
                carpeta_path = Path(carpeta)
                self.carpeta_destino = f"./Reportes/{carpeta_path.name}"
                
                # Guardar todos los archivos XML en un array
                self.archivosXML = [archivo for archivo in carpeta_path.glob("*.xml") if not archivo.name.startswith("R-")]
                
                if self.archivosXML:
                    # Cambiar color al label a negro en caso de que este en rojo
                    self.lblCargadosXML.config(foreground="black")
                    
                    print("Archivos seleccionados:", len(self.archivosXML))
                    
                    # Cambiar el valor de la etiqueta a 'estaSeleccionado'
                    self.estaSeleccionadoXML.set(f"Archivos Seleccionados: {len(self.archivosXML)} archivos")
                else:
                    self.estaSeleccionadoXML.set("No se encontraron archivos XML en la carpeta seleccionada")
                    self.lblCargadosXML.config(foreground="red")
            else:
                self.estaSeleccionadoXML.set("No se seleccionó ninguna carpeta")
                self.lblCargadosXML.config(foreground="red")
        else:
        
            # Abrir ventana emergente para seleccionar los archivos excel a subir
            self.archivosXML = filedialog.askopenfilenames(filetypes=[("Archivos XML", "*.xml")])
            
            # Comprobar si se han seleccionado archivos
            if self.archivosXML:
            
                if len(self.archivosXML) == 1:
                    archivosXML = Path(self.archivosXML[0])
                    
                    # Cambiar color al label a negro en caso de que este en rojo
                    self.lblCargadosXML.config(foreground="black")
                    
                    print("Archivos seleccionados:", self.archivosXML)
                    
                    # Cambiar el valor de la etiqueta a 'estaSeleccionado'
                    self.estaSeleccionadoXML.set(f"Archivo Seleccionado: {archivosXML.stem} ")
                
                else:
                    # Cambiar color al label a negro en caso de que este en rojo
                    self.lblCargadosXML.config(foreground="black")
                    
                    print("Archivos seleccionados:", self.archivosXML)
                    
                    # Cambiar el valor de la etiqueta a 'estaSeleccionado'
                    self.estaSeleccionadoXML.set(f"Archivos Seleccionados: {len(self.archivosXML)} archivos")
                    
            else:
                self.estaSeleccionadoXML.set("No se seleccionó archivo")
                self.lblCargadosXML.config(foreground="red")
    
    def btnConvertir_handler(self):
        # Limpiar diccionario
        self.datos_formulario.clear()
        self.reiniciar_progresoGeneral()
        
        # Ejecutar la carga de data en un hilo separado
        threading.Thread(target=self.convertir).start()

    def convertir(self):
        
        self.total = len(self.archivosXML)*2
        self.progreso["maximum"] = self.total
        
        for archivo in self.archivosXML:
            
            nombreArchivo = Path(archivo).stem
        
            tipoDoc = self.leer_XML(archivo)
            
            self.actualizar_progresoGeneral(self.total)
            
            # Verifica el tipo de documento y escoge la plantilla más apropiada
            match str(tipoDoc):
                case '01':
                    # Si nota_detracciones es diferente a '0' entonces escoge la plantilla 1
                    if self.datos_formulario['nota_detracciones'] != '0':
                        plantilla = 'plantillaFactura1.pdf'
                    else:
                        plantilla = 'plantillaFactura2.pdf'
                case '03':
                    plantilla = 'plantillaBoleta.pdf'
                case '07':
                    plantilla = 'plantillaNotaCredito.pdf'
                case '08':
                    plantilla = 'plantillaNotaDebito.pdf'
            
            self.rellenar_plantilla(plantilla, self.datos_formulario, nombreArchivo, tipoDoc)
            self.actualizar_progresoGeneral(self.total)
            
        if len(self.archivosXML) == 1:
            # Abrir ventana para abrir carpeta
            self.ventana_carpeta_generada(f'./Reportes/{nombreArchivo}/')
        else:
            if self.carpeta_destino != "":
                self.ventana_carpeta_generada(f'{self.carpeta_destino}/')
            else:
                self.ventana_carpeta_generada('./Reportes/')
        
        self.btnConvertir.state(['!disabled'])
        
        if self.errores:
            print(f"Hubo errores en los archivos: ")
            for e in self.errores:
                print("\n")
                print(e)

    # Función para copiar y luego rellenar el PDF
    def rellenar_plantilla(self, plantilla, datos_formulario, nombreArchivo, tipoDoc):
        try:
            self.carpeta_destino = f'./Reportes/{nombreArchivo}' if self.carpeta_destino == "" else self.carpeta_destino
            # Verificar si la carpeta de destino existe, si no, crearla
            if not os.path.exists(self.carpeta_destino):
                os.makedirs(self.carpeta_destino)

            # Crear la ruta completa del archivo con el nombre personalizado
            archivo_destino = Path(self.carpeta_destino) / f"{nombreArchivo}.pdf"

            form_fields = list(fillpdfs.get_form_fields(f'./plantillas/{plantilla}').keys())

            match tipoDoc:
                case '01':
                    if datos_formulario['nota_detracciones'] != '0':
                        
                        if datos_formulario['comentario'] != '0':
                            observacion =  datos_formulario['comentario']
                        else:
                            observacion = datos_formulario['observacion']
                                
                        data_dict = {
                            # Rellenar los campos del formulario en la copia
                            form_fields[2]: datos_formulario['doc'],
                            form_fields[0]: datos_formulario['nombre'],
                            form_fields[3]: datos_formulario['fecha'],
                            form_fields[1]: datos_formulario['documento'],
                            form_fields[24]: datos_formulario['direccion'],
                            form_fields[4]: datos_formulario['forma_pago'],
                            form_fields[6]: datos_formulario['item'],
                            form_fields[8]: datos_formulario['codigo'],
                            form_fields[7]: datos_formulario['descripcion'],
                            form_fields[5]: datos_formulario['und'],
                            form_fields[9]: datos_formulario['cantidad'],
                            form_fields[10]: datos_formulario['vUnitario'],
                            form_fields[11]: datos_formulario['pUnitario'],
                            form_fields[12]: datos_formulario['valorV'],
                            form_fields[22]: datos_formulario['numeroTexto'],
                            form_fields[14]: datos_formulario['opGravada'],
                            form_fields[15]: datos_formulario['igv'],
                            form_fields[13]: datos_formulario['total'],
                            form_fields[16]: datos_formulario['observacionesSunat'],
                            form_fields[18]: datos_formulario['direccionSucursal'],
                            form_fields[19]: datos_formulario['nota_detracciones'],
                            form_fields[17]: observacion,
                            form_fields[20]: datos_formulario['placa'],
                            form_fields[21]: datos_formulario['hash'],
                            form_fields[23]: datos_formulario['ruc'],
                        }
                        
                    else:
                        if datos_formulario['comentario'] != '0':
                            observacion = datos_formulario['comentario']
                        else:
                            observacion = datos_formulario['observacion'],
                        # Rellenar los campos del formulario en la copia
                        data_dict = {
                            form_fields[2]: datos_formulario['doc'],
                            form_fields[0]: datos_formulario['nombre'],
                            form_fields[3]: datos_formulario['fecha'],
                            form_fields[23]: datos_formulario['documento'],
                            form_fields[1]: datos_formulario['direccion'],
                            form_fields[4]: datos_formulario['forma_pago'],
                            form_fields[6]: datos_formulario['item'],
                            form_fields[8]: datos_formulario['codigo'],
                            form_fields[7]: datos_formulario['descripcion'],
                            form_fields[5]: datos_formulario['und'],
                            form_fields[9]: datos_formulario['cantidad'],
                            form_fields[10]: datos_formulario['vUnitario'],
                            form_fields[11]: datos_formulario['pUnitario'],
                            form_fields[12]: datos_formulario['valorV'],
                            form_fields[21]: datos_formulario['numeroTexto'],
                            form_fields[14]: datos_formulario['opGravada'],
                            form_fields[15]: datos_formulario['igv'],
                            form_fields[13]: datos_formulario['total'],
                            form_fields[16]: datos_formulario['observacionesSunat'],
                            form_fields[18]: datos_formulario['direccionSucursal'],
                            form_fields[17]: observacion,
                            form_fields[19]: datos_formulario['placa'],
                            form_fields[20]: datos_formulario['hash'],
                            form_fields[22]: datos_formulario['ruc']
                        }
                        
                case '03':
                    data_dict = {
                        form_fields[13]: datos_formulario['doc'],
                        form_fields[0]: datos_formulario['nombre'],
                        form_fields[21]: datos_formulario['fecha'],
                        form_fields[1]: datos_formulario['documento'],
                        form_fields[2]: datos_formulario['item'],
                        form_fields[3]: datos_formulario['codigo'],
                        form_fields[4]: datos_formulario['descripcion'],
                        form_fields[5]: datos_formulario['und'],
                        form_fields[6]: datos_formulario['cantidad'],
                        form_fields[8]: datos_formulario['vUnitario'],
                        form_fields[7]: datos_formulario['pUnitario'],
                        form_fields[10]: datos_formulario['valorV'],
                        form_fields[18]: datos_formulario['numeroTexto'],
                        form_fields[9]: datos_formulario['opGravada'],
                        form_fields[12]: datos_formulario['igv'],
                        form_fields[11]: datos_formulario['total'],
                        form_fields[14]: datos_formulario['observacionesSunat'],
                        form_fields[15]: datos_formulario['direccionSucursal'],
                        form_fields[16]: datos_formulario['observacion'],
                        form_fields[17]: datos_formulario['placa'],
                        form_fields[19]: datos_formulario['hash'],
                        form_fields[20]: datos_formulario['ruc'],
                    }
                case '07':
                    data_dict = {
                        form_fields[13]: datos_formulario['doc'],
                        form_fields[0]: datos_formulario['nombre'],
                        form_fields[18]: datos_formulario['fecha'],
                        form_fields[21]: datos_formulario['documento'],
                        form_fields[1]: datos_formulario['direccion'],
                        form_fields[19]: datos_formulario['documento_referencia'],
                        form_fields[2]: datos_formulario['item'],
                        form_fields[3]: datos_formulario['codigo'],
                        form_fields[4]: datos_formulario['descripcion'],
                        form_fields[5]: datos_formulario['und'],
                        form_fields[6]: datos_formulario['cantidad'],
                        form_fields[8]: datos_formulario['vUnitario'],
                        form_fields[7]: datos_formulario['pUnitario'],
                        form_fields[10]: datos_formulario['valorV'],
                        form_fields[20]: datos_formulario['numeroTexto'],
                        form_fields[9]: datos_formulario['opGravada'],
                        form_fields[12]: datos_formulario['igv'],
                        form_fields[11]: datos_formulario['total'],
                        form_fields[14]: datos_formulario['observacionesSunat'],
                        form_fields[15]: datos_formulario['motivo'],
                        form_fields[16]: datos_formulario['hash'],
                        form_fields[17]: datos_formulario['ruc'],
                    }
                case '08':
                    data_dict = {
                        form_fields[13]: datos_formulario['doc'],
                        form_fields[0]: datos_formulario['nombre'],
                        form_fields[18]: datos_formulario['fecha'],
                        form_fields[21]: datos_formulario['documento'],
                        form_fields[1]: datos_formulario['direccion'],
                        form_fields[19]: datos_formulario['documento_referencia'],
                        form_fields[2]: datos_formulario['item'],
                        form_fields[3]: datos_formulario['codigo'],
                        form_fields[4]: datos_formulario['descripcion'],
                        form_fields[5]: datos_formulario['und'],
                        form_fields[6]: datos_formulario['cantidad'],
                        form_fields[8]: datos_formulario['vUnitario'],
                        form_fields[7]: datos_formulario['pUnitario'],
                        form_fields[10]: datos_formulario['valorV'],
                        form_fields[20]: datos_formulario['numeroTexto'],
                        form_fields[9]: datos_formulario['opGravada'],
                        form_fields[12]: datos_formulario['igv'],
                        form_fields[11]: datos_formulario['total'],
                        form_fields[14]: datos_formulario['observacionesSunat'],
                        form_fields[15]: datos_formulario['motivo'],
                        form_fields[16]: datos_formulario['hash'],
                        form_fields[17]: datos_formulario['ruc']
                    }
            
            # Guardar el PDF rellenado
            fillpdfs.write_fillable_pdf( input_pdf_path= f'./plantillas/{plantilla}', output_pdf_path=archivo_destino, data_dict=data_dict, flatten=True)
                
        except Exception as e:
            print(f"Error en el archivo: {nombreArchivo}")
            print(e)
            
            self.errores.append(nombreArchivo)
        
    
    def leer_XML(self, archivo):
        tree = ET.parse(archivo)
        root = tree.getroot()
        
        namespaces = {
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        }
        
        # Verificar si existe el elemento cac:DiscrepancyResponse para saber si el documento
        # es nota de debito o credito
        discrepancy_response = root.find('cac:DiscrepancyResponse', namespaces)
        tipoDoc = root.find('cbc:InvoiceTypeCode', namespaces)
        
        try:

            # Comprobar si el elemento existe
            if discrepancy_response is not None:
                # Buscar el elemento ResponseCode dentro del nodo DiscrepancyResponse
                response_code = root.find('cac:DiscrepancyResponse//cbc:ResponseCode', namespaces)
                # Acceder al atributo listName
                list_name = response_code.attrib.get('listName')
                print(f"listName: {list_name}")
                if list_name in ['Tipo de nota de debito', 'Tipo de nota de débito']:
                    # Asignar el tipo de documento para el procesado
                    tipoDoc = '08'
                elif list_name in ['Tipo de nota de credito', 'Tipo de nota de crédito']:
                    tipoDoc = '07'
            if tipoDoc is not None:
                tipoDoc = tipoDoc.text
            else:    
                tipoDoc = root.find('.//cbc:DocumentTypeCode', namespaces).text
                
            match tipoDoc:
                case '01':
                    self.procesar_factura(root, archivo)
                case '03':
                    self.procesar_boleta(root, archivo)
                case '07':
                    self.procesar_nota_credito(root, archivo)
                case '08':
                    self.procesar_nota_debito(root, archivo)
            
            return tipoDoc
    
        except Exception as e:
            print(f"Ocurrio un error al leer el archivo {archivo}")
            self.errores.append(archivo)
    
    def procesar_nota_debito(self, root, archivo):
        # Definir el namespace para cbc y cac
        namespaces = {
            'xmlns': "urn:oasis:names:specification:ubl:schema:xsd:DebitNote-2",
            'biz': "urn:bizlinks:names:specification:ubl:peru:schema:xsd:BizlinksAggregateComponents-1",
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            'ds': "http://www.w3.org/2000/09/xmldsig#",
            'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
            'qdt': "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2",
            'sac': "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1"
        }
        # Fecha y Hora
        date = root.find("cbc:IssueDate", namespaces).text
        time = root.find("cbc:IssueTime", namespaces)
        
        # datetime.strptime(date.text, '%Y-%m-%d')
        if time is not None:
            time = time.text
            fechaEmision = f"{date} {time}"
        else:
            fechaEmision = f"{date}"
            
        print(f"Fecha emision: {fechaEmision}")

        # Código Hash
        hash = root.find('.//ds:DigestValue', namespaces).text
        print(f"hash: {hash}")

        # Nombre
        ## Buscar el valor de cbc:RegistrationName dentro de cac:AccountingCustomerParty
        nombre = root.find('.//cac:AccountingCustomerParty//cbc:RegistrationName', namespaces).text

        print(f'nombre: {nombre}') 
        
            
        # DNI
        documento = root.find('.//cac:AccountingCustomerParty//cbc:ID', namespaces).text
        print (f'documento: {documento}')
        doc = root.find('cbc:ID', namespaces)
        doc = doc.text
        print(f'doc: {doc}')
        
        # MOTIVO
        motivo = root.find('cac:DiscrepancyResponse//cbc:Description', namespaces).text
        print(f'motivo: {motivo}')
        
        #DOCUMENTO REFERENCIA
        documento_referencia = root.find('cac:BillingReference//cbc:ID', namespaces).text
        print(f'documento_referencia: {documento_referencia}')
        
        # Direccion
        direccion = root.find('cac:AccountingCustomerParty//cac:AddressLine//cbc:Line',namespaces).text if root.find('cac:AccountingCustomerParty//cac:AddressLine//cbc:Line',namespaces) is not None else '-'
        print(f'direccion: {direccion}')
        
        # Items
        ## Item
        item = root.find('.//cac:DebitNoteLine//cbc:ID', namespaces).text
        print(item)

        ## Código
        codigo = root.find('.//cac:DebitNoteLine//cac:Item//cbc:ID', namespaces)
        codigo = codigo.text if codigo is not None else item
        print(codigo)

        ## Descripción
        desc = root.find('.//cac:DebitNoteLine//cac:Item//cbc:Description', namespaces).text

        ## Und.
        und = root.find('.//cac:DebitNoteLine//cbc:DebitedQuantity', namespaces)
        und = und.attrib.get('unitCode')
        print(f'und: {und}')

        ## Cantidad
        cantidad = root.find('.//cac:DebitNoteLine//cbc:DebitedQuantity', namespaces).text
        cantidad = format(float(cantidad), '.2f')
        print(f'cantidad: {cantidad}')

        ## V. Unitario
        vUnitario = root.find('.//cac:DebitNoteLine//cbc:LineExtensionAmount', namespaces).text
        vUnitario = format(float(vUnitario), '.4f')
        print(f'vUnitario: {vUnitario}')

        ## P. Unitario
        pUnitario = root.find('.//cac:DebitNoteLine//cac:PricingReference//cbc:PriceAmount', namespaces).text
        pUnitario = format(float(pUnitario), '.2f')
        print(f'pUnitario: {pUnitario}')

        ## Valor Venta
        valorV = root.find('.//cac:DebitNoteLine//cac:Price//cbc:PriceAmount', namespaces).text
        print(f'valorV: {valorV}')
        
        ## Op Gravada
        opGravada = root.find('.//cac:TaxTotal//cac:TaxSubtotal//cbc:TaxableAmount', namespaces).text
        print(f'opGravada; {opGravada}')

        porcentaje = root.find('.//cac:TaxTotal//cac:TaxCategory//cbc:Percent', namespaces).text
        porcentaje = f"{porcentaje[:2]}%"

        igv = root.find('.//cac:TaxTotal//cac:TaxSubtotal//cbc:TaxAmount', namespaces).text
        igv = format(float(igv), '.2f')
        print(f'igv: {igv}')

        total = root.find('.//cac:RequestedMonetaryTotal//cbc:PayableAmount', namespaces).text
        total = format(float(total), '.2f')
        print(f'total: {total}')

        # Numero en texto
        # Numero en texto
        numeroTexto = root.find('cbc:Note', namespaces)
        
        numeroTexto = numeroTexto.text if numeroTexto is not None else self.numerosTexto.get(total)

        # Observaciones
        ## Invocar función para cargar el archivo con las observaciones, caso que no esté
        ## se busca el archivo y se descomprime
        treeR = self.cargar_observaciones_xml(archivo)
        rootR = treeR.getroot()
        observaciones = rootR.find('.//cac:DocumentResponse//cbc:Description', namespaces).text
        print(f'observaciones: {observaciones}')
        
        # R.U.C
        ruc = root.find('cac:Signature//cac:SignatoryParty//cbc:ID', namespaces)
        ruc = ruc.text if ruc is not None else '20517252558'
        ruc = f'{ruc}-{doc}'
        
        self.datos_formulario = {'fecha': fechaEmision, 'nombre': nombre, 'doc': doc, 'documento': documento, 'direccion': direccion, 'motivo': motivo, 'documento_referencia': documento_referencia, 'item': item, 'codigo': codigo, 
                                'descripcion': desc, 'und': und, 'cantidad': cantidad, 'vUnitario': vUnitario, 'pUnitario': pUnitario, 
                                'valorV': valorV, 'numeroTexto': numeroTexto, 'opGravada': opGravada, 'igv': igv, 'total': total, 'observacionesSunat': observaciones,
                                'hash': hash, 'ruc': ruc}
    
    def procesar_nota_credito(self, root, archivo):
        # Definir el namespace para cbc y cac
        namespaces = {
            'xmlns': "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2",
            'biz': "urn:bizlinks:names:specification:ubl:peru:schema:xsd:BizlinksAggregateComponents-1",
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            'ds': "http://www.w3.org/2000/09/xmldsig#",
            'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
            'qdt': "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2",
            'sac': "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1"
        }
        # Fecha y Hora
        date = root.find("cbc:IssueDate", namespaces).text
        time = root.find("cbc:IssueTime", namespaces)
        
        # datetime.strptime(date.text, '%Y-%m-%d')
        if time is not None:
            time = time.text
            fechaEmision = f"{date} {time}"
        else:
            fechaEmision = f"{date}"
            
        print(f"Fecha emision: {fechaEmision}")

        # Código Hash
        hash = root.find('.//ds:DigestValue', namespaces).text
        print(f"hash: {hash}")

        # Nombre
        ## Buscar el valor de cbc:RegistrationName dentro de cac:AccountingCustomerParty
        nombre = root.find('.//cac:AccountingCustomerParty//cbc:RegistrationName', namespaces).text

        print(f'nombre: {nombre}') 
        
            
        # DNI
        documento = root.find('.//cac:AccountingCustomerParty//cbc:ID', namespaces).text
        print (f'documento: {documento}')
        doc = root.find('cbc:ID', namespaces)
        doc = doc.text
        print(f'doc: {doc}')
        
        # MOTIVO
        motivo = root.find('cac:DiscrepancyResponse//cbc:Description', namespaces).text
        print(f'motivo: {motivo}')
        
        #DOCUMENTO REFERENCIA
        documento_referencia = root.find('cac:BillingReference//cbc:ID', namespaces).text
        print(f'documento_referencia: {documento_referencia}')
        
        # Direccion
        direccion = root.find('cac:AccountingCustomerParty//cac:AddressLine//cbc:Line',namespaces).text if root.find('cac:AccountingCustomerParty//cac:AddressLine//cbc:Line',namespaces) is not None else '-'
        print(f'direccion: {direccion}')
        
        # Items
        ## Item
        item = root.find('.//cac:CreditNoteLine//cbc:ID', namespaces).text
        print(item)

        ## Código
        codigo = root.find('.//cac:CreditNoteLine//cac:Item//cbc:ID', namespaces)
        codigo = codigo.text if codigo is not None else item
        print(codigo)

        ## Descripción
        desc = root.find('.//cac:CreditNoteLine//cac:Item//cbc:Description', namespaces).text

        ## Und.
        und = root.find('.//cac:CreditNoteLine//cbc:CreditedQuantity', namespaces)
        und = und.attrib.get('unitCode')
        print(f'und: {und}')

        ## Cantidad
        cantidad = root.find('.//cac:CreditNoteLine//cbc:CreditedQuantity', namespaces).text
        cantidad = format(float(cantidad), '.2f')
        print(f'cantidad: {cantidad}')

        ## V. Unitario
        vUnitario = root.find('.//cac:CreditNoteLine//cbc:LineExtensionAmount', namespaces).text
        vUnitario = format(float(vUnitario), '.4f')
        print(f'vUnitario: {vUnitario}')

        ## P. Unitario
        pUnitario = root.find('.//cac:CreditNoteLine//cac:PricingReference//cbc:PriceAmount', namespaces).text
        pUnitario = format(float(pUnitario), '.2f')
        print(f'pUnitario: {pUnitario}')

        ## Valor Venta
        valorV = root.find('.//cac:CreditNoteLine//cac:Price//cbc:PriceAmount', namespaces).text
        print(f'valorV: {valorV}')
        
        ## Op Gravada
        opGravada = root.find('.//cac:TaxTotal//cac:TaxSubtotal//cbc:TaxableAmount', namespaces).text
        print(f'opGravada; {opGravada}')

        porcentaje = root.find('.//cac:TaxTotal//cac:TaxCategory//cbc:Percent', namespaces).text
        porcentaje = f"{porcentaje[:2]}%"

        igv = root.find('.//cac:TaxTotal//cac:TaxSubtotal//cbc:TaxAmount', namespaces).text
        igv = format(float(igv), '.2f')
        print(f'igv: {igv}')

        total = root.find('.//cac:LegalMonetaryTotal//cbc:PayableAmount', namespaces).text
        total = format(float(total), '.2f')
        print(f'total: {total}')

        # Numero en texto
        # Numero en texto
        numeroTexto = root.find('cbc:Note', namespaces)
        
        numeroTexto = numeroTexto.text if numeroTexto is not None else self.numerosTexto.get(total)

        # Observaciones
        ## Invocar función para cargar el archivo con las observaciones, caso que no esté
        ## se busca el archivo y se descomprime
        treeR = self.cargar_observaciones_xml(archivo)
        rootR = treeR.getroot()
        observaciones = rootR.find('.//cac:DocumentResponse//cbc:Description', namespaces).text
        print(f'observaciones: {observaciones}')
        
        # R.U.C
        ruc = root.find('cac:Signature//cac:SignatoryParty//cbc:ID', namespaces)
        ruc = ruc.text if ruc is not None else '20517252558'
        ruc = f'{ruc}-{doc}'
        
        self.datos_formulario = {'fecha': fechaEmision, 'nombre': nombre, 'doc': doc, 'documento': documento, 'direccion': direccion, 'motivo': motivo, 'documento_referencia': documento_referencia, 'item': item, 'codigo': codigo, 
                                'descripcion': desc, 'und': und, 'cantidad': cantidad, 'vUnitario': vUnitario, 'pUnitario': pUnitario, 
                                'valorV': valorV, 'numeroTexto': numeroTexto, 'opGravada': opGravada, 'igv': igv, 'total': total, 'observacionesSunat': observaciones,
                                'hash': hash, 'ruc': ruc}
    
    def procesar_factura(self, root, archivo):
        # Definir el namespace para cbc y cac
        namespaces = {
            'xmlns': "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
            'biz': "urn:bizlinks:names:specification:ubl:peru:schema:xsd:BizlinksAggregateComponents-1",
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            'ds': "http://www.w3.org/2000/09/xmldsig#",
            'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
            'qdt': "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2",
            'sac': "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1"
        }
        
        # Fecha y Hora
        date = root.find("cbc:IssueDate", namespaces).text
        time = root.find("cbc:IssueTime", namespaces)
        
        # datetime.strptime(date.text, '%Y-%m-%d')
        if time is not None:
            time = time.text
            fechaEmision = f"{date} {time}"
        else:
            fechaEmision = f"{date}"
            
        print(f"Fecha emision: {fechaEmision}")

        # Código Hash
        hash = root.find('.//ds:DigestValue', namespaces).text
        print(f"hash: {hash}")

        # Nombre
        ## Buscar el valor de cbc:RegistrationName dentro de cac:AccountingCustomerParty
        nombre = root.find('.//cac:AccountingCustomerParty//cbc:RegistrationName', namespaces).text

        print(f'nombre: {nombre}') 
            
        # DNI
        documento = root.find('.//cac:AccountingCustomerParty//cbc:ID', namespaces).text
        print (f'documento: {documento}')
        # Documento boleta, factura etc
        doc = root.find('cbc:ID', namespaces)
        doc = doc.text
        print(f'doc: {doc}')
        
        # Direccion
        direccion = root.find('cac:AccountingCustomerParty//cac:AddressLine//cbc:Line',namespaces).text if root.find('cac:AccountingCustomerParty//cac:AddressLine//cbc:Line',namespaces) is not None else '-'
        print(f'direccion: {direccion}')
        
        # Forma de pago
        forma_pago = root.find('cac:PaymentTerms//cbc:PaymentMeansID', namespaces)
        forma_pago = forma_pago.text if forma_pago is not None else "Contado"
        print(f'forma_pago: {forma_pago}')
        
        # Items
        ## Item
        item = root.find('.//cac:InvoiceLine//cbc:ID', namespaces).text
        print(item)

        ## Código
        codigo = root.find('.//cac:InvoiceLine//cac:Item//cbc:ID', namespaces)
        codigo = codigo.text if codigo is not None else item
        print(codigo)

        ## Descripción
        desc = root.find('.//cac:InvoiceLine//cac:Item//cbc:Description', namespaces).text

        ## Und.
        und = root.find('.//cac:InvoiceLine//cbc:InvoicedQuantity', namespaces)
        und = und.attrib.get('unitCode')
        print(f'und: {und}')

        ## Cantidad
        cantidad = root.find('.//cac:InvoiceLine//cbc:InvoicedQuantity', namespaces).text
        cantidad = format(float(cantidad), '.2f')
        print(f'cantidad: {cantidad}')

        ## V. Unitario
        vUnitario = root.find('.//cac:InvoiceLine//cbc:LineExtensionAmount', namespaces).text
        vUnitario = format(float(vUnitario), '.4f')
        print(f'vUnitario: {vUnitario}')

        ## P. Unitario
        pUnitario = root.find('.//cac:InvoiceLine//cac:PricingReference//cbc:PriceAmount', namespaces).text
        pUnitario = format(float(pUnitario), '.2f')
        print(f'pUnitario: {pUnitario}')

        ## Valor Venta
        valorV = root.find('.//cac:InvoiceLine//cac:Price//cbc:PriceAmount', namespaces).text
        print(f'valorV: {valorV}')
        # Moneda
        opGravada = root.find('.//cac:TaxTotal//cac:TaxSubtotal//cbc:TaxableAmount', namespaces).text
        print(f'opGravada; {opGravada}')

        # porcentaje = root.find('.//cac:TaxTotal//cac:TaxCategory//cbc:Percent', namespaces).text
        # porcentaje = f"{porcentaje[:2]}%"

        igv = root.find('.//cac:TaxTotal//cac:TaxSubtotal//cbc:TaxAmount', namespaces).text
        igv = format(float(igv), '.2f')
        print(f'igv: {igv}')

        total = root.find('.//cac:LegalMonetaryTotal//cbc:PayableAmount', namespaces).text
        total = format(float(total), '.2f')
        print(f'total: {total}')

        # Numero en texto
        numeroTexto = root.find('cbc:Note', namespaces)
        
        numeroTexto = numeroTexto.text if numeroTexto is not None else self.numerosTexto.get(total)

        # Observaciones
        ## Invocar función para cargar el archivo con las observaciones, caso que no esté
        ## se busca el archivo y se descomprime
        treeR = self.cargar_observaciones_xml(archivo)
        
        if treeR != None:
            rootR = treeR.getroot()
            observaciones = rootR.find('.//cac:DocumentResponse//cbc:Description', namespaces).text
            print(f'observaciones: {observaciones}')
        else:
            observaciones = '0'
        
        # Informacion Adicional
        additional_properties = root.findall('.//ext:ExtensionContent//biz:AdditionalProperty', namespaces)
            
        additional_data = []
        direccionSucursal = self.peaje_nombres.get(doc[1]) if self.peaje_nombres.get(doc[1]) != None else '0'
        observacion = 'MANEJE CON CUIDADO SU VIDA ES MUY VALIOSA'
        placa = '0'
        comentario = '0'
        nota_detracciones = '0'
        
        for prop in additional_properties:
            id_value = prop.find('cbc:ID', namespaces).text
            value = prop.find('cbc:Value', namespaces).text
            additional_data.append({'ID': id_value, 'Value': value})
            
        for i in additional_data:
            id_value = int(i['ID'])
            value = i['Value']
            
            # Direccion de la Sucursal
            if id_value == 9785:
                direccionSucursal = value if value is not None else direccionSucursal
            # Placa
            elif id_value == 9114:
                placa = value
            # Observación
            elif id_value == 9618:
                observacion = value if value != 'MANEJE CON CUIDADO SU VIDA ES MUY VALIOSA' else observacion
            # Comentario
            elif id_value == 9510:
                comentario = value
            # Nota - Defracciones
            elif id_value == 9752:
                nota_detracciones = value
            
        print(placa)
        print(direccionSucursal)
        print(observacion)
        print(f'comentario: {comentario}')
        print(f'nota_detracciones: {nota_detracciones}')
        
        # R.U.C
        ruc = root.find('cac:Signature//cac:SignatoryParty//cbc:ID', namespaces)
        ruc = ruc.text if ruc is not None else '20517252558'
        ruc = f'{ruc}-{doc}'
        
        self.datos_formulario = {'fecha': fechaEmision, 'nombre': nombre, 'doc': doc, 'documento': documento, 'direccion': direccion, 'forma_pago': forma_pago, 'item': item, 'codigo': codigo, 
                                'descripcion': desc, 'und': und, 'cantidad': cantidad, 'vUnitario': vUnitario, 'pUnitario': pUnitario, 
                                'valorV': valorV, 'numeroTexto': numeroTexto, 'opGravada': opGravada, 'igv': igv, 'total': total, 'observacionesSunat': observaciones,
                                'direccionSucursal': direccionSucursal, 'observacion': observacion, 'comentario': comentario, 'nota_detracciones': nota_detracciones, 'placa': placa, 'hash': hash, 'ruc': ruc}

    def procesar_boleta(self, root, archivo):
        namespaces = {
            'xmlns': "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
            'biz': "urn:bizlinks:names:specification:ubl:peru:schema:xsd:BizlinksAggregateComponents-1",
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            'ds': "http://www.w3.org/2000/09/xmldsig#",
            'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
            'qdt': "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2",
            'sac': "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1"
        }
        
        # Fecha y Hora
        date = root.find("cbc:IssueDate", namespaces).text
        time = root.find("cbc:IssueTime", namespaces)
        
        # datetime.strptime(date.text, '%Y-%m-%d')
        if time is not None:
            time = time.text
            fechaEmision = f"{date} {time}"
        else:
            fechaEmision = f"{date}"
            
        print(f"Fecha emision: {fechaEmision}")

        # Código Hash
        hash = root.find('.//ds:DigestValue', namespaces).text
        print(f"hash: {hash}")

        # Nombre
        ## Buscar el valor de cbc:RegistrationName dentro de cac:AccountingCustomerParty
        nombre = root.find('.//cac:AccountingCustomerParty//cbc:RegistrationName', namespaces)
        nombre = nombre.text if nombre is not None else 'Consumidor Final'

        print(f'nombre: {nombre}') 
        
            
        # DNI
        documento = root.find('.//cac:AccountingCustomerParty//cbc:ID', namespaces).text
        print (f'documento: {documento}')
        # Documento boleta, factura etc
        doc = root.find('cbc:ID', namespaces)
        doc = doc.text
        print(f'doc: {doc}')
        
        # Direccion
        direccion = root.find('cac:AccountingCustomerParty//cac:AddressLine//cbc:Line',namespaces).text if root.find('cac:AccountingCustomerParty//cac:AddressLine//cbc:Line',namespaces) is not None else '-'
        print(f'direccion: {direccion}')
        
        # Items
        ## Item
        item = root.find('.//cac:InvoiceLine//cbc:ID', namespaces).text
        print(item)

        ## Código
        codigo = root.find('.//cac:InvoiceLine//cac:Item//cbc:ID', namespaces)
        codigo = codigo.text if codigo is not None else item
        print(codigo)

        ## Descripción
        desc = root.find('.//cac:InvoiceLine//cac:Item//cbc:Description', namespaces).text

        ## Und.
        und = root.find('.//cac:InvoiceLine//cbc:InvoicedQuantity', namespaces)
        und = und.attrib.get('unitCode')
        print(f'und: {und}')

        ## Cantidad
        cantidad = root.find('.//cac:InvoiceLine//cbc:InvoicedQuantity', namespaces).text
        cantidad = format(float(cantidad), '.2f')
        print(f'cantidad: {cantidad}')

        ## V. Unitario
        vUnitario = root.find('.//cac:InvoiceLine//cbc:LineExtensionAmount', namespaces).text
        vUnitario = format(float(vUnitario), '.4f')
        print(f'vUnitario: {vUnitario}')

        ## P. Unitario
        pUnitario = root.find('.//cac:InvoiceLine//cac:PricingReference//cbc:PriceAmount', namespaces).text
        pUnitario = format(float(pUnitario), '.2f')
        print(f'pUnitario: {pUnitario}')

        ## Valor Venta
        valorV = root.find('.//cac:InvoiceLine//cac:Price//cbc:PriceAmount', namespaces).text
        print(f'valorV: {valorV}')
        # Moneda
        opGravada = root.find('.//cac:TaxTotal//cac:TaxSubtotal//cbc:TaxableAmount', namespaces).text
        print(f'opGravada; {opGravada}')

        porcentaje = root.find('.//cac:TaxTotal//cac:TaxCategory//cbc:Percent', namespaces).text
        porcentaje = f"{porcentaje[:2]}%"

        igv = root.find('.//cac:TaxTotal//cac:TaxSubtotal//cbc:TaxAmount', namespaces).text
        igv = format(float(igv), '.2f')
        print(f'igv: {igv}')

        total = root.find('.//cac:LegalMonetaryTotal//cbc:PayableAmount', namespaces).text
        total = format(float(total), '.2f')
        print(f'total: {total}')

        # Numero en texto
        # Numero en texto
        numeroTexto = root.find('cbc:Note', namespaces)
        
        numeroTexto = numeroTexto.text if numeroTexto is not None else self.numerosTexto.get(total)

        # Observaciones
        ## Invocar función para cargar el archivo con las observaciones, caso que no esté
        ## se busca el archivo y se descomprime
        treeR = self.cargar_observaciones_xml(archivo)
        if treeR is not None:
            rootR = treeR.getroot()
            observaciones = rootR.find('.//cac:DocumentResponse//cbc:Description', namespaces).text
            print(f'observaciones: {observaciones}')
        else:
            observaciones = '0'
        
        # Informacion Adicional
        additional_properties = root.findall('.//ext:ExtensionContent//biz:AdditionalProperty', namespaces)
        additional_data = []
        direccionSucursal = self.peaje_nombres.get(doc[1]) if self.peaje_nombres.get(doc[1]) != None else '0'
        observacion = 'MANEJE CON CUIDADO SU VIDA ES MUY VALIOSA'
        placa = '0'
        
        for prop in additional_properties:
            id_value = prop.find('cbc:ID', namespaces).text
            value = prop.find('cbc:Value', namespaces).text
            additional_data.append({'ID': id_value, 'Value': value})
            
        for i in additional_data:
            id_value = int(i['ID'])
            value = i['Value']
            
            # Direccion de la Sucursal
            if id_value == 9785:
                direccionSucursal = value if value is not None else direccionSucursal
            # Placa
            elif id_value == 9114:
                placa = value
            # Observación
            elif id_value == 9618:
                observacion = value if value != 'MANEJE CON CUIDADO SU VIDA ES MUY VALIOSA' else observacion
                
        print(placa)
        print(direccionSucursal)
        print(observacion)
        
        # R.U.C
        ruc = root.find('cac:Signature//cac:SignatoryParty//cbc:ID', namespaces)
        ruc = ruc.text if ruc is not None else '20517252558'
        ruc = f'{ruc}-{doc}'
        
        self.datos_formulario = {'fecha': fechaEmision, 'nombre': nombre, 'doc': doc, 'documento': documento, 'direccion': direccion, 'item': item, 'codigo': codigo, 
                                'descripcion': desc, 'und': und, 'cantidad': cantidad, 'vUnitario': vUnitario, 'pUnitario': pUnitario, 
                                'valorV': valorV, 'numeroTexto': numeroTexto, 'opGravada': opGravada, 'igv': igv, 'total': total, 'observacionesSunat': observaciones,
                                'direccionSucursal': direccionSucursal, 'observacion': observacion, 'placa': placa, 'hash': hash, 'ruc': ruc}
    
    def cargar_observaciones_xml(self, archivo):
        archivo_ruta = Path(archivo)  # Convertir a objeto Path para manejar rutas
        archivoR = f"R-{archivo_ruta.stem}"

        # Obtener la ruta base del archivo
        carpeta_base = archivo_ruta.parent

        # Construir la ruta completa hacia la carpeta y el archivo XML asociado
        ruta_completa_archivoR = carpeta_base / archivoR / f"{archivoR}.xml"

        try:
            # Intentar cargar el archivo XML
            treeR = ET.parse(ruta_completa_archivoR)
            print(f"Archivo XML encontrado y cargado: {ruta_completa_archivoR}")
            return treeR
        except FileNotFoundError:
            print(f"No se encontró el archivo XML en {ruta_completa_archivoR}, buscando archivo xml...")

            # Si no se encuentra el archivo XML, buscar un archivo comprimido en la misma carpeta
            archivo_zip = carpeta_base / f"{archivoR}.zip"
            archivo_xml = carpeta_base / f"{archivoR}.xml"
            if archivo_xml.exists():
                treeR = ET.parse(archivo_xml)
                print(f"Archivo XML encontrado y cargado: {archivo_xml}")
                return treeR
            if archivo_zip.exists():
                print(f"Archivo comprimido encontrado: {archivo_zip}")
                
                # Crear una carpeta para descomprimir
                carpeta_destino = carpeta_base / archivoR
                os.makedirs(carpeta_destino, exist_ok=True)

                # Descomprimir el archivo ZIP
                with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
                    zip_ref.extractall(carpeta_destino)

                # Intentar cargar el archivo XML descomprimido
                ruta_completa_archivoR = carpeta_destino / f"{archivoR}.xml"
                try:
                    treeR = ET.parse(ruta_completa_archivoR)
                    print(f"Archivo XML descomprimido y cargado: {ruta_completa_archivoR}")
                    return treeR
                except FileNotFoundError:
                    print(f"No se pudo encontrar el archivo XML dentro del archivo descomprimido: {ruta_completa_archivoR}")
                    return None
            else:
                print(f"No se encontró ningún archivo comprimido con el nombre {archivoR}.zip en {carpeta_base}")
                return None
    
    def ventana_carpeta_generada(self, ruta_archivo):
        
        # Especificar el tamaño de la ventana
        ancho_ventana = 200
        alto_ventana = 100
        
        # Crear una nueva ventana
        ventana = Toplevel(self.root)
        ventana.title("Abrir carpeta")
        
        # Establecer el tamaño de la ventana
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

        etiqueta = Label(ventana, text="¿Desea abrir la carpeta generada?")
        etiqueta.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        
        # Botón para confirmar apertura del archivo
        boton_confirmar = ttk.Button(ventana, text="Sí", command=lambda: self.confirmar_abrir_archivo(ventana, ruta_archivo))
        boton_confirmar.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        
        # Botón para cancelar (cerrar la ventana sin abrir el archivo)
        boton_cancelar = ttk.Button(ventana, text="No", command=ventana.destroy)
        boton_cancelar.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        
        # Vincular la tecla Enter al botón de confirmación
        ventana.bind('<Return>', lambda event: boton_confirmar.invoke())
        # Vincular la tecla Esc para cerrar la ventana
        ventana.bind('<Escape>', lambda event: ventana.destroy())
        
        # Centrar ventana
        self.centrar_ventana(ventana, ancho_ventana, alto_ventana)
    
    def confirmar_abrir_archivo(self, ventana, ruta_archivo):
        # Obtener la carpeta del archivo
        carpeta = os.path.dirname(ruta_archivo)
        
        # Abrir la carpeta 
        try:
            os.startfile(f'{os.getcwd()}{carpeta}')
        except Exception as e:
            print(f"No se pudo abrir la carpeta:")
            print(e)
        
        # Cerrar la ventana
        ventana.destroy()
        