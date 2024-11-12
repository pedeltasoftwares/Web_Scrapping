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

# Solicitar la ruta de almacenamiento y la URL al usuario
ruta_documentos = input("Introduce la ruta donde deseas almacenar el archivo HTML: ")
nueva_url = input("Introduce la URL que deseas abrir en una nueva pestaña: ")

# Abrir la nueva URL en una nueva pestaña
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(nueva_url)


download_files(driver,ruta_documentos)


