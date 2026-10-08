# Pre-entrega Automation Testing – SauceDemo

## Propósito del proyecto
Automatizar con **Selenium WebDriver y Python** los flujos básicos de navegación de [saucedemo.com](https://www.saucedemo.com), una app demo pensada para prácticas de testing:

1. **Login exitoso** con `standard_user` / `secret_sauce`. Valida redirección a `/inventory.html` y los textos "Products" y "Swag Labs".
2. **Navegación y verificación del catálogo**. Valida título, presencia de productos, nombre y precio del primero, y elementos de la interfaz (menú, filtro, carrito).
3. **Carrito de compras**. Agrega el primer producto, verifica el contador del carrito y que el producto aparezca en el carrito con el mismo nombre y precio.

Los tests son independientes entre sí: cada uno abre su propio navegador, por lo que la falla de uno no afecta a los demás.

## Tecnologías utilizadas
- Python 3.10+
- Selenium WebDriver
- Pytest
- pytest-html (reportes HTML)
- Git y GitHub

## Estructura del proyecto
```
├── tests/
│   └── test_saucedemo.py   # Casos de prueba
├── utils/
│   ├── config.py           # URLs, credenciales, tiempos y localizadores
│   └── helpers.py          # Funciones auxiliares (driver, login, esperas, capturas)
├── reports/                # Reporte HTML, logs y capturas de pantalla
├── conftest.py             # Fixtures y captura automática en fallos
├── pytest.ini              # Configuración de Pytest y logs
├── requirements.txt
└── README.md
```

## Instalación de dependencias
Requiere Google Chrome instalado (Selenium descarga el driver automáticamente).

```bash
# 1. Clonar el repositorio
git clone https://github.com/estefania-pose/pre-entrega-automation-testing-Estefania-Pose.git
cd pre-entrega-automation-testing-<Estefania-Pose>

# 2. (Opcional) Crear entorno virtual
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Cómo ejecutar las pruebas
```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Para correr sin abrir la ventana del navegador:
```bash
# Linux / Mac
HEADLESS=1 pytest -v --html=reports/reporte.html --self-contained-html

# Windows (PowerShell)
$env:HEADLESS=1; pytest -v --html=reports/reporte.html --self-contained-html
```

## Evidencias generadas
- `reports/reporte.html`: reporte HTML con el resultado de cada test.
- `reports/ejecucion.log`: log de la ejecución.
- `reports/screenshots/`: capturas automáticas cuando un test falla (también se adjuntan al reporte HTML).
