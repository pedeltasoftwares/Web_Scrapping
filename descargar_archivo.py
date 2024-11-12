from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil

def download_files(driver,carpeta_destino):
    """
    Función para verificar si existe un botón de descarga (btn_Descargar)
    en la página actual y, si existe, hacer clic en él para descargar el archivo.
    """
    # Ruta de la carpeta de descargas (ajusta según tu sistema y configuración)
    carpeta_descargas = "D:\Descargas"

    #Verifica si hay botones de descargar
    try:
        # Espera hasta que al menos un botón de descarga esté presente en la página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-xs.btn-primary.descargaArchivo"))
        )
        botones_descargar = driver.find_elements(By.CSS_SELECTOR, "button.btn.btn-xs.btn-primary.descargaArchivo")
        num_btns = len(botones_descargar)
    except:
        num_btns = 0

    #Verifica si hay divs
    try:
        # Espera hasta que al menos un botón de descarga esté presente en la página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tooltipp.col-lg-2.col-md-3.col-sm-4.col-xs-6"))
        )
        divs_secundarios = driver.find_elements(By.CSS_SELECTOR, "div.tooltipp.col-lg-2.col-md-3.col-sm-4.col-xs-6")
        num_divs = len(divs_secundarios)
    except:
        num_divs = 0

    # Verificar si existen elementos <li> para la paginación
    try:
        # Esperar hasta que el div de paginación esté presente en la página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.dataTables_paginate.paging_simple_numbers li a[href*='page']"))
        )
        elementos_paginacion = driver.find_elements(By.CSS_SELECTOR, "div.dataTables_paginate.paging_simple_numbers li a[href*='page']")
        num_paginas = len(elementos_paginacion)
    except:
        num_paginas = 0

    ###
    ### ACCIÓN PARA LOS BOTONES DE DESCARGA
    ###

    if num_btns > 0:
        # Hacer clic en cada botón de descarga encontrado
        for boton in botones_descargar:
            
            try:
                #Hace click
                boton.click()

                time.sleep(2)
                # Espera a que el archivo aparezca en la carpeta de descargas
                archivo_descargado = esperar_descarga(carpeta_descargas)
                
                if archivo_descargado:
                    # Mueve el archivo descargado a la carpeta de destino
                    ruta_origen = os.path.join(carpeta_descargas, archivo_descargado)
                    ruta_destino = os.path.join(carpeta_destino, archivo_descargado)
                    shutil.move(ruta_origen, ruta_destino)
                    time.sleep(2)
                    print(f"Archivo {archivo_descargado} movido a {carpeta_destino}")
            except:
                driver.refresh()
                time.sleep(2)


    ###
    ### ACCIÓN PARA LAS DIVISIONES
    ###

    if num_divs > 0:
        titulos_carpetas = get_titulo_divs(divs_secundarios)
        i = 0
        for division in divs_secundarios:

            #Crea la ruta de subcarpeta
            ruta_sub = f'{carpeta_destino}\\{titulos_carpetas[i]}'
            crear_subcarpeta(ruta_sub)

        # Encuentra el enlace dentro del div y abre en una nueva pestaña
            link = division.find_element(By.TAG_NAME, "a")
            driver.execute_script("window.open(arguments[0].href);", link)

            # Cambiar a la nueva pestaña
            driver.switch_to.window(driver.window_handles[-1])

            # Espera explícita para asegurarse de que la página haya cambiado de contexto y cargado
            WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

            # Confirmación del cambio de contexto (opcional para depuración)
            print("URL actual en la nueva pestaña:", driver.current_url)

            #descarga los archivos
            download_files(driver,ruta_sub)

            # Cierra la pestaña actual y vuelve a la principal
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

            i+=1

    ###
    ### ACCIÓN PARA LAS PAGINACIONES
    ###
    if num_paginas > 0:
        # Obtener la URL actual
        url_base = driver.current_url

        # Iterar sobre cada página que necesitas abrir
        for i in range(2, num_paginas + 1):  # Empieza desde 2 porque ya estamos en la primera página
            # Construir la URL con el iterador en el parámetro `page`
            nueva_url = f"{url_base}?page={i}"
            print(f"Abrir nueva pestaña para la URL: {nueva_url}")

            # Abrir una nueva pestaña con la URL modificada
            driver.execute_script(f"window.open('{nueva_url}', '_blank');")

            # Cambiar a la nueva pestaña
            driver.switch_to.window(driver.window_handles[-1])

            # Esperar a que la página cargue completamente antes de interactuar
            WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

            # Encontrar los botones de descarga en la nueva página y proceder a la descarga
            botones_descarga_paginacion = driver.find_elements(By.CSS_SELECTOR, "button.btn.btn-xs.btn-primary.descargaArchivo")
            download_page_files(botones_descarga_paginacion, carpeta_descargas, carpeta_destino)

            # Cerrar la pestaña actual después de la descarga y volver a la principal
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])


#DESCARGAR ARCHIVOS DE PAGINACIÓN
def download_page_files(botones_descarga_paginacion,carpeta_descargas,carpeta_destino):

    for boton in botones_descarga_paginacion:
        #Hace click
        boton.click()

        time.sleep(2)
        # Espera a que el archivo aparezca en la carpeta de descargas
        archivo_descargado = esperar_descarga(carpeta_descargas)
    
        if archivo_descargado:
            # Mueve el archivo descargado a la carpeta de destino
            ruta_origen = os.path.join(carpeta_descargas, archivo_descargado)
            ruta_destino = os.path.join(carpeta_destino, archivo_descargado)
            shutil.move(ruta_origen, ruta_destino)
            time.sleep(2)
            print(f"Archivo {archivo_descargado} movido a {carpeta_destino}")




### CREA SUBCARPETA
def crear_subcarpeta(ruta):
    try:
        os.mkdir(ruta)
    except OSError:
        pass


#OBTIENE TITULOS DE DIVS
def get_titulo_divs(divs):
    """
    Función que obtiene los nombres de los divs
    """
    titulos_carpetas = []

    for div in divs:
        if div.text:
            titulos_carpetas.append(div.text)  # Agregar el texto a la lista, sin espacios extra

    return titulos_carpetas

#ESPERAR DESCARGA
def esperar_descarga(carpeta_descargas):
    """
    Función que espera hasta que un nuevo archivo aparezca en la carpeta de descargas y
    ya no esté en uso (descarga completada).
    """
    archivo_descargado = None
    continuar = True
    while continuar:

        # Obtiene la lista de archivos en la carpeta de descargas, ordenada por última modificación
        archivos = [f for f in os.listdir(carpeta_descargas)]
        # Verificar si alguno de los archivos tiene la extensión .crdownload
        descargas_incompletas = [f for f in archivos if f.endswith('.crdownload')]

        if not descargas_incompletas:
            archivos = [f for f in os.listdir(carpeta_descargas)]
            archivos = sorted(archivos, key=lambda x: os.path.getmtime(os.path.join(carpeta_descargas, x)), reverse=True)
            archivo_descargado = archivos[0]
            continuar = False

    return archivo_descargado

      