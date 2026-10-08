"""
Pre-entrega: automatización de saucedemo.com con Selenium WebDriver + Pytest.

Casos incluidos:
  1. Login exitoso
  2. Navegación y verificación del catálogo
  3. Agregar un producto al carrito y verificarlo

Cada test usa su propio navegador (ver conftest.py), por eso son independientes.
"""
import logging

from utils import config
from utils.helpers import (
    agregar_producto_al_carrito,
    esperar_url_contiene,
    esperar_visible,
    hacer_login,
    obtener_datos_producto,
    obtener_primer_producto,
)

logger = logging.getLogger(__name__)


def test_login_exitoso(driver):
    """Login con credenciales válidas: redirige a /inventory.html y muestra 'Products' / 'Swag Labs'."""
    hacer_login(driver)

    # Validación 1: URL del inventario
    assert config.RUTA_INVENTARIO in driver.current_url, (
        f"Se esperaba estar en {config.RUTA_INVENTARIO} pero la URL es {driver.current_url}"
    )

    # Validación 2: título de la sección
    titulo = esperar_visible(driver, config.TITULO_PAGINA).text
    assert titulo == config.TITULO_INVENTARIO, (
        f"Se esperaba el título '{config.TITULO_INVENTARIO}' y apareció '{titulo}'"
    )

    # Validación 3: logo de la app
    logo = esperar_visible(driver, config.LOGO_APP).text
    assert logo == config.NOMBRE_APP, (
        f"Se esperaba el logo '{config.NOMBRE_APP}' y apareció '{logo}'"
    )


def test_catalogo_navegacion_y_elementos(driver_logueado):
    """Verifica título, presencia de productos y elementos clave de la interfaz."""
    driver = driver_logueado

    # Título correcto de la página de inventario
    titulo = esperar_visible(driver, config.TITULO_PAGINA).text
    assert titulo == config.TITULO_INVENTARIO, f"Título incorrecto: '{titulo}'"

    # Hay al menos un producto visible
    productos = driver.find_elements(*config.PRODUCTOS)
    assert len(productos) > 0, "No se encontraron productos en el inventario"

    # Nombre y precio del primer producto
    nombre, precio = obtener_datos_producto(productos[0])
    logger.info("Primer producto: %s - %s", nombre, precio)
    print(f"Primer producto: {nombre} - {precio}")
    assert nombre != "", "El primer producto no tiene nombre"
    assert precio.startswith("$"), f"El precio no tiene formato esperado: '{precio}'"

    # Elementos importantes de la interfaz: menú, filtro y carrito
    assert driver.find_element(*config.MENU_HAMBURGUESA).is_displayed(), "No se muestra el menú"
    assert driver.find_element(*config.FILTRO_ORDEN).is_displayed(), "No se muestra el filtro de orden"
    assert driver.find_element(*config.ICONO_CARRITO).is_displayed(), "No se muestra el ícono del carrito"


def test_agregar_producto_al_carrito(driver_logueado):
    """Agrega el primer producto, verifica el contador y que aparezca en el carrito."""
    driver = driver_logueado

    # Guardamos nombre y precio del primer producto antes de agregarlo
    primer_producto = obtener_primer_producto(driver)
    assert primer_producto is not None, "No hay productos para agregar al carrito"
    nombre_esperado, precio_esperado = obtener_datos_producto(primer_producto)

    # Agregar al carrito
    agregar_producto_al_carrito(primer_producto)

    # El contador del carrito debe pasar a 1
    contador = esperar_visible(driver, config.CONTADOR_CARRITO).text
    assert contador == "1", f"El contador del carrito debería ser '1' y es '{contador}'"

    # Ir al carrito
    driver.find_element(*config.ICONO_CARRITO).click()
    esperar_url_contiene(driver, config.RUTA_CARRITO)

    # Debe haber exactamente un ítem y coincidir con el agregado
    items = driver.find_elements(*config.ITEMS_CARRITO)
    assert len(items) == 1, f"Se esperaba 1 ítem en el carrito y hay {len(items)}"

    nombre_carrito, precio_carrito = obtener_datos_producto(items[0])
    assert nombre_carrito == nombre_esperado, (
        f"Nombre en carrito '{nombre_carrito}' distinto del agregado '{nombre_esperado}'"
    )
    assert precio_carrito == precio_esperado, (
        f"Precio en carrito '{precio_carrito}' distinto del esperado '{precio_esperado}'"
    )
