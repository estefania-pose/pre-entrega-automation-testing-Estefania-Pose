"""
Configuración central del proyecto: URLs, credenciales, tiempos y localizadores.
Si cambia algo en la página, se corrige acá y no en cada test.
"""
from selenium.webdriver.common.by import By

# --- Datos del sitio ---
URL_BASE = "https://www.saucedemo.com/"
RUTA_INVENTARIO = "/inventory.html"
RUTA_CARRITO = "/cart.html"

# --- Credenciales válidas (publicadas por el propio sitio demo) ---
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"

# --- Textos esperados ---
TITULO_INVENTARIO = "Products"
NOMBRE_APP = "Swag Labs"

# --- Tiempo máximo de espera explícita (segundos) ---
TIMEOUT_ESPERA = 10

# --- Localizadores: Login ---
CAMPO_USUARIO = (By.ID, "user-name")
CAMPO_PASSWORD = (By.ID, "password")
BOTON_LOGIN = (By.ID, "login-button")

# --- Localizadores: Inventario ---
LOGO_APP = (By.CLASS_NAME, "app_logo")
TITULO_PAGINA = (By.CLASS_NAME, "title")
PRODUCTOS = (By.CLASS_NAME, "inventory_item")
NOMBRE_PRODUCTO = (By.CLASS_NAME, "inventory_item_name")
PRECIO_PRODUCTO = (By.CLASS_NAME, "inventory_item_price")
BOTON_AGREGAR = (By.CSS_SELECTOR, "button.btn_inventory")
MENU_HAMBURGUESA = (By.ID, "react-burger-menu-btn")
FILTRO_ORDEN = (By.CLASS_NAME, "product_sort_container")
ICONO_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
CONTADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")

# --- Localizadores: Carrito ---
ITEMS_CARRITO = (By.CLASS_NAME, "cart_item")
