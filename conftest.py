"""
Fixtures y hooks compartidos por todos los tests.
- driver: navegador nuevo por cada test (así los tests son independientes).
- driver_logueado: navegador con el login ya hecho.
- Hook: si un test falla, guarda captura de pantalla y la adjunta al reporte HTML.
"""
import pytest

from utils.helpers import capturar_pantalla, crear_driver, hacer_login

try:
    from pytest_html import extras
except ImportError:  # pytest-html no instalado
    extras = None


@pytest.fixture
def driver():
    """Abre un navegador limpio para cada test y lo cierra al terminar."""
    navegador = crear_driver()
    yield navegador
    navegador.quit()


@pytest.fixture
def driver_logueado(driver):
    """Navegador con sesión iniciada con standard_user."""
    hacer_login(driver)
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si el test falla, toma una captura y la agrega al reporte HTML."""
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when == "call" and reporte.failed:
        navegador = item.funcargs.get("driver")
        if navegador is not None:
            capturar_pantalla(navegador, item.name)
            if extras is not None:
                reporte.extras = getattr(reporte, "extras", []) + [
                    extras.png(navegador.get_screenshot_as_base64())
                ]
