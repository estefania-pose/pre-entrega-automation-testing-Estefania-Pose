"""
Funciones auxiliares reutilizables por los tests:
creación del driver, login, esperas explícitas, capturas y acciones sobre productos.
"""
import logging
import os
import re
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import config

logger = logging.getLogger(__name__)

CARPETA_CAPTURAS = os.path.join("reports", "screenshots")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def crear_driver():
    """Crea un Chrome nuevo. Con la variable de entorno HEADLESS=1 corre sin ventana."""
    opciones = Options()
    if os.getenv("HEADLESS") == "1":
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1920,1080")
    # Evita los popups de Chrome sobre contraseñas que pueden tapar elementos
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=opciones)
    logger.info("Driver de Chrome creado")
    return driver


# ---------------------------------------------------------------------------
# Esperas explícitas
# ---------------------------------------------------------------------------
def esperar_visible(driver, localizador, timeout=config.TIMEOUT_ESPERA):
    """Espera a que un elemento sea visible y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(localizador)
    )


def esperar_url_contiene(driver, texto, timeout=config.TIMEOUT_ESPERA):
    """Espera a que la URL actual contenga un texto determinado."""
    return WebDriverWait(driver, timeout).until(EC.url_contains(texto))


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------
def hacer_login(driver, usuario=config.USUARIO_VALIDO, password=config.PASSWORD_VALIDO):
    """Abre saucedemo.com, completa las credenciales y espera la redirección al inventario."""
    logger.info("Navegando a %s", config.URL_BASE)
    driver.get(config.URL_BASE)

    esperar_visible(driver, config.CAMPO_USUARIO).send_keys(usuario)
    driver.find_element(*config.CAMPO_PASSWORD).send_keys(password)
    driver.find_element(*config.BOTON_LOGIN).click()
    logger.info("Credenciales enviadas para el usuario '%s'", usuario)

    esperar_url_contiene(driver, config.RUTA_INVENTARIO)
    logger.info("Redirigido a la página de inventario")


# ---------------------------------------------------------------------------
# Productos
# ---------------------------------------------------------------------------
def obtener_primer_producto(driver):
    """Devuelve el primer producto del inventario como elemento web."""
    productos = driver.find_elements(*config.PRODUCTOS)
    return productos[0] if productos else None


def obtener_datos_producto(producto):
    """Devuelve (nombre, precio) de un elemento de producto."""
    nombre = producto.find_element(*config.NOMBRE_PRODUCTO).text
    precio = producto.find_element(*config.PRECIO_PRODUCTO).text
    return nombre, precio


def agregar_producto_al_carrito(producto):
    """Hace clic en el botón 'Add to cart' del producto indicado."""
    producto.find_element(*config.BOTON_AGREGAR).click()
    logger.info("Producto agregado al carrito")


# ---------------------------------------------------------------------------
# Evidencias
# ---------------------------------------------------------------------------
def capturar_pantalla(driver, nombre_test):
    """Guarda una captura en reports/screenshots y devuelve la ruta del archivo."""
    os.makedirs(CARPETA_CAPTURAS, exist_ok=True)
    nombre_limpio = re.sub(r"[^\w\-]", "_", nombre_test)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = os.path.join(CARPETA_CAPTURAS, f"{nombre_limpio}_{marca_tiempo}.png")
    driver.save_screenshot(ruta)
    logger.error("Captura de pantalla guardada en %s", ruta)
    return ruta
