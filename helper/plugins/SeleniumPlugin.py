"""
=============================================================================
Módulo: SeleniumPlugin.py
Descripción: Plugin que gestiona el ciclo de vida del navegador (WebDriver).
             Se encarga de:
             - Inicializar el navegador antes de cada escenario
             - Configurar opciones del navegador (cookies, timeouts, resolución)
             - Cerrar el navegador después de cada escenario

Tipos de ejecución soportados:
    - "localhost": Usa drivers locales almacenados en el proyecto
    - "manager":  Usa WebDriverManager para descargar drivers automáticamente

Navegadores soportados:
    - Chrome (local y manager)
    - Firefox (solo local)
    - Safari (solo macOS, local)
=============================================================================
"""

import os        # Acceso a variables de entorno
import platform  # Detectar sistema operativo (Windows, Darwin/macOS, Linux)
import pathlib   # Manejo de rutas de archivos multiplataforma

from dotenv import load_dotenv  # Carga variables desde archivo .env al entorno
from selenium import webdriver  # Módulo principal de Selenium WebDriver

# Servicios para configurar la ruta del driver de cada navegador
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.firefox.service import Service as FirefoxService

# WebDriver Manager: descarga automática de drivers compatibles
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager

# Importaciones internas del framework
from helper.plugins import PluginSpec          # Especificación de hooks (decoradores)
from helper.selenium_class.elements import Elements  # Clase de esperas y búsqueda de elementos

# Nota: Las siguientes clases se importaban pero no existen aún en el proyecto.
# Se comentan para evitar errores de importación:
# from helper.selenium_class.js_script import JsScript
# from helper.selenium_class.keyboard_actions import KeyboardActions
# from helper.selenium_class.mouse_actions import MouseActions
# from helper.selenium_class.window_control import WindowControl


def execution_selenium(context):
    """
    Función principal que orquesta la inicialización del navegador.

    Lee la variable de entorno EXECUTION_TYPE para decidir cómo crear
    el WebDriver y lo asigna al contexto de Behave para que esté
    disponible en todos los steps.

    Args:
        context: Objeto de Behave donde se almacena el estado compartido.
                 Después de esta función, context tendrá:
                 - context.browser: instancia del WebDriver
                 - context.elements: instancia de Elements para buscar elementos

    Flujo:
        1. Imprime información del entorno (OS, tipo ejecución, navegador)
        2. Según EXECUTION_TYPE, crea el driver con la estrategia correspondiente
        3. Configura el navegador (cookies, timeouts, ventana)
        4. Inyecta las clases helper en el contexto
    """
    # Información de diagnóstico para debugging en consola
    print("> Sistema Operativo:", platform.system())
    print("> Tipo de ejecución:", os.getenv('EXECUTION_TYPE'))
    print("> Navegador:", os.getenv('BROWSER'))

    # Lee el tipo de ejecución desde .env
    exec_type = os.getenv('EXECUTION_TYPE')

    # Selecciona la estrategia de creación del driver
    if exec_type == "localhost":
        # Usa drivers binarios almacenados localmente en el proyecto
        context.browser = config_driver_local(context)
    elif exec_type == "manager":
        # Usa WebDriverManager para descargar el driver automáticamente
        context.browser = config_driver_webdriver_manager(context)
    else:
        # Si el valor no es válido, falla con mensaje claro
        raise AssertionError("EXECUTION_TYPE no válido. Revisa README.md")

    # === Configuración post-creación del navegador ===

    # Elimina todas las cookies para empezar con sesión limpia
    context.browser.delete_all_cookies()

    # Espera implícita global: si un elemento no se encuentra inmediatamente,
    # Selenium esperará hasta 20 segundos antes de lanzar error
    context.browser.implicitly_wait(20)

    # Maximiza la ventana del navegador para evitar problemas de responsive
    context.browser.maximize_window()

    # Timeout máximo para carga de página completa (15 segundos)
    context.browser.set_page_load_timeout(15)

    # === Inyección de clases helper en el contexto ===

    # Elements: proporciona métodos de espera explícita y búsqueda de elementos
    context.elements = Elements(context.browser)


def build_driver_path(browser: str, name_os: str) -> str:
    """
    Construye la ruta absoluta hacia el ejecutable del driver local.

    Los drivers están organizados en carpetas por navegador y sistema operativo:
    helper/selenium_class/web_driver/{navegador}/{sistema_operativo}/

    Args:
        browser (str): Nombre del navegador ("chrome", "firefox", etc.)
        name_os (str): Sistema operativo ("Darwin", "Windows", "Linux")

    Returns:
        str: Ruta absoluta al directorio del driver.

    Ejemplo:
        build_driver_path("chrome", "Darwin")
        → "/Users/user/proyecto/helper/selenium_class/web_driver/chrome/Darwin/"
    """
    # pathlib.Path().absolute() obtiene la ruta del directorio de trabajo actual
    base_path = pathlib.Path().absolute()
    driver_path = f"{base_path}/helper/selenium_class/web_driver/{browser}/{name_os}/"
    # Reemplaza backslashes de Windows por forward slashes (compatibilidad)
    return driver_path.replace("\\", "/")


def config_driver_local(context):
    """
    Configura el WebDriver utilizando binarios (drivers) almacenados localmente.

    Esta estrategia es útil cuando:
    - No hay acceso a internet para descargar drivers
    - Se necesita una versión específica del driver
    - Se trabaja en un entorno controlado/corporativo

    Args:
        context: Objeto de Behave (no se usa directamente aquí).

    Returns:
        WebDriver: Instancia del navegador configurado.

    Raises:
        Exception: Si el navegador no está soportado o Safari se ejecuta fuera de macOS.
    """
    browser = os.getenv("BROWSER")           # Lee navegador desde .env
    name_os = platform.system()              # Detecta OS: "Darwin" (macOS), "Windows", "Linux"

    # Construye la ruta al directorio donde está el driver
    driver_path = build_driver_path(browser, name_os)

    if browser == "chrome":
        # ChromeService recibe la ruta al ejecutable chromedriver
        # ChromeOptions permite configurar argumentos del navegador
        return webdriver.Chrome(
            service=ChromeService(executable_path=driver_path + "chromedriver"),
            options=webdriver.ChromeOptions()
        )
    elif browser == "firefox":
        # Similar a Chrome pero con geckodriver (driver de Firefox)
        return webdriver.Firefox(
            service=FirefoxService(executable_path=driver_path + "geckodriver"),
            options=webdriver.FirefoxOptions()
        )
    elif browser == "safari":
        # Safari solo funciona en macOS y no necesita driver externo
        if platform.system() != "Darwin":
            raise Exception("Safari solo está disponible en macOS")
        return webdriver.Safari()
    else:
        raise Exception(f"Navegador local no soportado: {browser}")


def config_driver_webdriver_manager(context):
    """
    Configura Selenium usando WebDriverManager para descarga automática de drivers.

    WebDriverManager detecta la versión del navegador instalado y descarga
    automáticamente el driver compatible. Es la opción más cómoda para
    desarrollo local ya que no requiere gestionar drivers manualmente.

    Args:
        context: Objeto de Behave donde se almacena el browser.

    Returns:
        WebDriver: Instancia de Chrome configurada.

    Raises:
        Exception: Si el navegador solicitado no está soportado por el manager.
    """
    browser = os.getenv("BROWSER", "chrome").lower()

    # Configuración de opciones de Chrome
    options = webdriver.ChromeOptions()

    # "eager": no espera a que se carguen todos los recursos (imágenes, CSS)
    # Solo espera al DOM. Acelera la ejecución de pruebas.
    options.page_load_strategy = "eager"

    # Opciones para estabilidad en entornos CI/CD (Jenkins, GitLab CI, etc.)
    options.add_argument("--disable-dev-shm-usage")  # Evita errores de memoria compartida
    options.add_argument("--no-sandbox")              # Necesario para ejecutar como root
    options.add_argument("--disable-gpu")             # Evita errores de GPU en servidores
    options.add_argument("--headless=new")            # Ejecuta sin interfaz gráfica (necesario en CI)
    options.add_argument("--window-size=1920,1080")   # Resolución fija para screenshots consistentes
    options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detección de bot
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    if browser == "chrome":
        # Intenta usar ChromeDriverManager para descargar el driver
        # Si falla (ej: en CI con Chrome preinstalado), usa Chrome directamente
        try:
            service = Service(ChromeDriverManager().install())
            context.browser = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"> WebDriverManager falló ({e}), usando Chrome del sistema...")
            context.browser = webdriver.Chrome(options=options)
    else:
        raise Exception(f"Navegador no soportado por WebDriver Manager: {browser}")
    return context.browser


class SeleniumPlugin:
    """
    Plugin de Selenium para el framework de pruebas.

    Implementa los hooks before_scenario y after_scenario definidos en PluginSpec.
    Se registra en environment.py y se ejecuta automáticamente en cada escenario.

    Responsabilidades:
        - before_scenario: Carga .env, inicializa el navegador
        - after_scenario: Cierra el navegador y libera recursos

    Ejemplo de flujo:
        1. Behave encuentra un Scenario en el .feature
        2. environment.py llama pm.hook.before_scenario()
        3. pluggy ejecuta SeleniumPlugin.before_scenario()
        4. Se crea el navegador y se asigna a context.browser
        5. Se ejecutan los steps del escenario
        6. environment.py llama pm.hook.after_scenario()
        7. pluggy ejecuta SeleniumPlugin.after_scenario()
        8. Se cierra el navegador con quit()
    """

    @PluginSpec.hookimpl
    def before_scenario(self, context, scenario):
        """
        Hook que se ejecuta ANTES de cada escenario.

        Acciones:
            1. Carga las variables de entorno desde el archivo .env
            2. Inicializa el navegador según la configuración
            3. Imprime el nombre del escenario para trazabilidad
        """
        load_dotenv(dotenv_path=".env", override=True)
        execution_selenium(context)
        print("Iniciando escenario:", scenario.name)

    @PluginSpec.hookimpl
    def after_scenario(self, context, scenario):
        """
        Hook que se ejecuta DESPUÉS de cada escenario.

        Acciones:
            1. Cierra el navegador (quit libera el proceso del driver)
            2. Imprime el resultado del escenario

        Args:
            context: Objeto compartido de Behave.
            scenario: Objeto del escenario con status (passed/failed/skipped).
        """
        if context.browser is not None:
            # quit() cierra el navegador Y termina el proceso del driver
            # A diferencia de close() que solo cierra la pestaña actual
            context.browser.quit()

        print("Finalizó escenario:", scenario.name, "| Estado:", scenario.status)
