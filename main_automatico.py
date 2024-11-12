from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from pathlib import Path
from descargar_archivo import download_files
from selenium.webdriver.support.ui import WebDriverWait
import os
import shutil

#rut ade documentos 
ruta_documentos = str(Path.home() / "Documents")
try: 
    os.mkdir(f'{ruta_documentos}\\web scrapping\\files\\')
except OSError:
    pass

# Configuración inicial del navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")


# Inicializar el driver de Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Ir a la página de inicio de sesión
url = "https://l2mbdataroom.metrodebogota.gov.co/"
driver.get(url)

# Encontrar el elemento de entrada por su atributo 'name'
input_usuario = driver.find_element(By.NAME, "Usuario")
input_usuario.send_keys("katherine.gonzalez@pedelta.com.co")

# Obtener el HTML de la página después de iniciar sesión
password = driver.find_element(By.NAME, "Contrasena")
password.send_keys("Metro.1999")

html_content = driver.page_source

# Analizar el HTML con BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Encuentra todos los divs con la clase específica
divs_principal = driver.find_elements(By.CSS_SELECTOR, "div.tooltipp.col-lg-2.col-md-3.col-sm-4.col-xs-6")

print("URL actual en la nueva pestaña:", driver.current_url)

# Lista para almacenar los textos extraídos de los divs de la página principal
titulos_carpetas = []
for div in divs_principal:
    if div.text:
        titulos_carpetas.append(div.text)  # Agregar el texto a la lista, sin espacios extra

# Iterar sobre cada div y hacer clic en el enlace dentro de cada uno
i = 25
for div in divs_principal[25:]:

    #Crea el nombre de carpeta
    rut_acumulada = f'{ruta_documentos}\\web scrapping\\files\\{titulos_carpetas[i]}'
    try: 
        os.mkdir(rut_acumulada)
    except OSError:
        pass

    #Elimina todo su contenido
    for archivo in os.listdir(rut_acumulada):
        ruta_archivo = os.path.join(rut_acumulada, archivo)
        if os.path.isfile(ruta_archivo) or os.path.islink(ruta_archivo):
            os.unlink(ruta_archivo)  # Elimina el archivo o enlace
        elif os.path.isdir(ruta_archivo):
            shutil.rmtree(ruta_archivo)  # Elimina el subdirectorio y su contenido

        
    # Encuentra el enlace dentro del div y abre en una nueva pestaña
    link = div.find_element(By.TAG_NAME, "a")
    driver.execute_script("window.open(arguments[0].href);", link)

    # Cambiar a la nueva pestaña
    driver.switch_to.window(driver.window_handles[-1])

    # Espera explícita para asegurarse de que la página haya cambiado de contexto y cargado
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # Confirmación del cambio de contexto (opcional para depuración)
    print("URL actual en la nueva pestaña:", driver.current_url)

    # Llama a la función para verificar y descargar el archivo
    download_files(driver,rut_acumulada)

    # Cierra la pestaña actual y vuelve a la principal
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # Espera después de cerrar la pestaña
    time.sleep(5)  # Tiempo de espera después de regresar

    i+=1

        
# Cerrar el navegador
driver.quit()




