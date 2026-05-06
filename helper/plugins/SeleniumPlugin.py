"""
Módulo: SeleniumPlugin.py
Descripción: Plugin que gestiona el ciclo de vida del navegador (WebDriver).

Tipos de ejecución soportados:
    - "localhost": Usa drivers locales almacenados en el proyecto
    - "manager":  Usa WebDriverManager para descargar drivers automáticamente
"""

import os
import platform
import pathlib

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager

from helper.plugins import PluginSpec
from helper.selenium_class.elements import Elements


def execution_selenium(context):
    """
    Orquesta la inicialización del navegador según EXECUTION_TYPE.
    Configura el browser y lo inyecta en el contexto de Behave.
    """
    print("> Sistema Operativo:", platform.system())
    print("> Tipo de ejecución:", os.getenv('EXECUTION_TYPE'))
    print("> Navegador:", os.getenv('BROWSER'))

    exec_type = os.getenv('EXECUTION_TYPE')

    if exec_type == "localhost":
        context.browser = config_driver_local(context)
    elif exec_type == "manager":
        context.browser = config_driver_webdriver_manager(context)
    else:
        raise AssertionError("EXECUTION_TYPE no válido. Revisa README.md")

    context.browser.delete_all_cookies()
    context.browser.implicitly_wait(20)
    context.browser.maximize_window()
    context.browser.set_page_load_timeout(15)
    context.elements = Elements(context.browser)


def build_driver_path(browser: str, name_os: str) -> str:
    """Construye la ruta absoluta hacia el ejecutable del driver local."""
    base_path = pathlib.Path().absolute()
    driver_path = f"{base_path}/helper/selenium_class/web_driver/{browser}/{name_os}/"
    return driver_path.replace("\\", "/")


def config_driver_local(context):
    """Configura el WebDriver utilizando binarios locales por sistema operativo."""
    browser = os.getenv("BROWSER")
    name_os = platform.system()
    driver_path = build_driver_path(browser, name_os)

    if browser == "chrome":
        return webdriver.Chrome(
            service=ChromeService(executable_path=driver_path + "chromedriver"),
            options=webdriver.ChromeOptions()
        )
    elif browser == "firefox":
        return webdriver.Firefox(
            service=FirefoxService(executable_path=driver_path + "geckodriver"),
            options=webdriver.FirefoxOptions()
        )
    elif browser == "safari":
        if platform.system() != "Darwin":
            raise Exception("Safari solo está disponible en macOS")
        return webdriver.Safari()
    else:
        raise Exception(f"Navegador local no soportado: {browser}")


def config_driver_webdriver_manager(context):
    """Configura Selenium usando WebDriverManager con descarga automática de drivers."""
    browser = os.getenv("BROWSER", "chrome").lower()

    options = webdriver.ChromeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    if browser == "chrome":
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
    """Plugin que inicializa y cierra el navegador en cada escenario."""

    @PluginSpec.hookimpl
    def before_scenario(self, context, scenario):
        load_dotenv(dotenv_path=".env", override=True)
        execution_selenium(context)
        print("Iniciando escenario:", scenario.name)

    @PluginSpec.hookimpl
    def after_scenario(self, context, scenario):
        if context.browser is not None:
            context.browser.quit()
        print("Finalizó escenario:", scenario.name, "| Estado:", scenario.status)
