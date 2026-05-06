"""
=============================================================================
Módulo: AllurePlugin.py
Descripción: Plugin que integra Allure Report con el framework de pruebas.
             Allure es una herramienta de reportería que genera reportes HTML
             interactivos con capturas de pantalla, pasos, y métricas.

Funcionalidades:
    - Captura screenshots automáticos después de cada step
    - Genera archivo environment.properties con datos del entorno de ejecución
    - Genera executors.json con información de quién ejecutó las pruebas
    - Copia historial previo para alimentar la sección Trend del reporte
=============================================================================
"""

import allure  # SDK de Allure para Python - permite adjuntar evidencia a los reportes
from allure_commons.types import AttachmentType  # Enum con tipos de adjuntos (PNG, TXT, HTML, etc.)

import os       # Acceso a variables de entorno
import json     # Para generar archivos JSON (executors.json)
import shutil   # Operaciones de archivos (copiar directorios)
from platform import system  # Detectar sistema operativo
import pathlib  # Manejo de rutas de archivos

from dotenv import load_dotenv  # Carga variables desde .env

from helper.plugins import PluginSpec  # Especificación de hooks del framework

# Rutas base del proyecto
BASE_PATH = str(pathlib.Path().absolute())
ALLURE_RESULTS_PATH = os.path.join(BASE_PATH, "report", "allure-results")
ALLURE_HISTORY_PATH = os.path.join(BASE_PATH, "report", "history")


def attachment_screenshot_step_in_allure(context):
    """
    Captura una screenshot del navegador y la adjunta al reporte de Allure.

    Esta función se ejecuta después de CADA step (Given/When/Then),
    proporcionando evidencia visual del estado de la aplicación en cada paso.

    Args:
        context: Objeto de Behave que contiene context.browser (WebDriver).
    """
    try:
        allure.attach(
            context.browser.get_screenshot_as_png(),  # Captura la pantalla como bytes PNG
            name="screenshot",                         # Nombre que aparece en el reporte
            attachment_type=AttachmentType.PNG          # Tipo de archivo adjunto
        )
    except Exception:
        # Si el navegador ya se cerró o hay error, no interrumpir la ejecución
        pass


def generate_environment_properties():
    """
    Genera el archivo environment.properties dentro de allure-results.

    Este archivo aparece en la sección "Environment" del reporte HTML
    y muestra información del entorno donde se ejecutaron las pruebas.
    """
    env_file = os.path.join(ALLURE_RESULTS_PATH, "environment.properties")
    with open(env_file, "w") as file:
        file.write(f"Browser : {os.getenv('BROWSER', 'chrome').capitalize()}\n")
        file.write(f"Browser.Version : Latest\n")
        file.write(f"Execution.Type : {os.getenv('EXECUTION_TYPE', 'N/A')}\n")
        file.write(f"URL : {os.getenv('URL', 'N/A')}\n")
        file.write(f"OS : {system()}\n")
        file.write(f"Executor : {os.getenv('EXECUTOR_NAME', 'N/A')}\n")


def generate_executor_json():
    """
    Genera el archivo executor.json dentro de allure-results.

    Este archivo alimenta la sección "Executors" del reporte de Allure,
    mostrando quién o qué sistema ejecutó las pruebas.

    Los valores se leen de variables de entorno para que cada alumno
    pueda personalizarlo desde su archivo .env:
        - EXECUTOR_NAME: Nombre del ejecutor (ej: "Juan Pérez")
        - EXECUTOR_BUILD_NAME: Nombre del build/rol (ej: "QA Automatizador")
        - EXECUTOR_TYPE: Tipo de ejecución (ej: "local", "jenkins", "gitlab")
    """
    executor_data = [
        {
            "name": os.getenv("EXECUTOR_NAME", "Automatizador"),
            "buildName": os.getenv("EXECUTOR_BUILD_NAME", "Ejecución Local"),
            "type": os.getenv("EXECUTOR_TYPE", "local")
        }
    ]

    executor_file = os.path.join(ALLURE_RESULTS_PATH, "executor.json")
    with open(executor_file, "w") as file:
        json.dump(executor_data, file, indent=2, ensure_ascii=False)


def copy_history_for_trends():
    """
    Copia el historial de ejecuciones previas a allure-results/history.

    Allure usa esta carpeta para generar los gráficos de TENDENCIA (Trends):
    - history-trend.json: Tendencia de passed/failed/broken por ejecución
    - duration-trend.json: Duración de cada ejecución
    - categories-trend.json: Tendencia de categorías de errores
    - retry-trend.json: Tendencia de reintentos

    Flujo para mantener el historial:
        1. Antes de ejecutar: se copia report/history → allure-results/history
        2. Se ejecutan las pruebas (genera nuevos resultados en allure-results)
        3. Allure genera el reporte y actualiza report/history con los nuevos datos
        4. En la próxima ejecución, el paso 1 incluirá el historial acumulado

    Sin este paso, la sección Trend siempre mostraría solo la última ejecución.
    """
    history_dest = os.path.join(ALLURE_RESULTS_PATH, "history")

    # Solo copiar si existe historial previo
    if os.path.exists(ALLURE_HISTORY_PATH):
        # Si ya existe la carpeta destino, la eliminamos para evitar conflictos
        if os.path.exists(history_dest):
            shutil.rmtree(history_dest)
        # Copia toda la carpeta de historial
        shutil.copytree(ALLURE_HISTORY_PATH, history_dest)
        print("> Historial de trends copiado para Allure")
    else:
        print("> No se encontró historial previo (primera ejecución)")


class AllurePlugin:
    """
    Plugin de Allure para el framework de pruebas.

    Implementa hooks del ciclo de vida de Behave para:
    - Preparar historial y metadata antes de las pruebas (before_all)
    - Capturar evidencia después de cada step (after_step)
    - Generar archivos de entorno y executor al finalizar (after_all)
    """

    @PluginSpec.hookimpl
    def before_all(self):
        """
        Hook ejecutado UNA VEZ antes de todas las pruebas.

        Acciones:
            1. Carga variables de entorno desde .env
            2. Crea la carpeta allure-results si no existe
            3. Copia el historial previo para alimentar los gráficos de Trend
        """
        load_dotenv(dotenv_path='.env')

        # Asegurar que existe la carpeta de resultados
        os.makedirs(ALLURE_RESULTS_PATH, exist_ok=True)

        # Copiar historial para que Allure genere los gráficos de tendencia
        copy_history_for_trends()

    @PluginSpec.hookimpl
    def after_step(self, context):
        """
        Hook ejecutado DESPUÉS de cada step (Given/When/Then).

        Captura automáticamente una screenshot del estado actual del navegador
        y la adjunta al reporte de Allure.

        Args:
            context: Objeto de Behave con el browser activo.
        """
        attachment_screenshot_step_in_allure(context)

    @PluginSpec.hookimpl
    def after_all(self, context):
        """
        Hook ejecutado UNA VEZ después de todas las pruebas.

        Genera los archivos de metadata para el reporte:
            - environment.properties → sección "Environment"
            - executor.json → sección "Executors"

        Args:
            context: Objeto de Behave.
        """
        generate_environment_properties()
        generate_executor_json()
