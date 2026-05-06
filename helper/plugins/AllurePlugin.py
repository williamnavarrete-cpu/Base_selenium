"""
Módulo: AllurePlugin.py
Descripción: Plugin que integra Allure Report con el framework de pruebas.
             Captura screenshots después de cada step y genera metadata del entorno.
"""

import os
import json
import shutil
import pathlib

import allure
from allure_commons.types import AttachmentType
from platform import system
from dotenv import load_dotenv

from helper.plugins import PluginSpec

BASE_PATH = str(pathlib.Path().absolute())
ALLURE_RESULTS_PATH = os.path.join(BASE_PATH, "report", "allure-results")
ALLURE_HISTORY_PATH = os.path.join(BASE_PATH, "report", "history")


def attachment_screenshot_step_in_allure(context):
    """Captura screenshot del navegador y la adjunta al reporte de Allure."""
    try:
        allure.attach(
            context.browser.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=AttachmentType.PNG
        )
    except Exception:
        pass


def generate_environment_properties():
    """Genera environment.properties para la sección Environment del reporte."""
    env_file = os.path.join(ALLURE_RESULTS_PATH, "environment.properties")
    with open(env_file, "w") as file:
        file.write(f"Browser : {os.getenv('BROWSER', 'chrome').capitalize()}\n")
        file.write(f"Browser.Version : Latest\n")
        file.write(f"Execution.Type : {os.getenv('EXECUTION_TYPE', 'N/A')}\n")
        file.write(f"URL : {os.getenv('URL', 'N/A')}\n")
        file.write(f"OS : {system()}\n")
        file.write(f"Executor : {os.getenv('EXECUTOR_NAME', 'N/A')}\n")


def generate_executor_json():
    """Genera executor.json para la sección Executors del reporte."""
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
    """Copia historial previo a allure-results/history para gráficos de tendencia."""
    history_dest = os.path.join(ALLURE_RESULTS_PATH, "history")

    if os.path.exists(ALLURE_HISTORY_PATH):
        if os.path.exists(history_dest):
            shutil.rmtree(history_dest)
        shutil.copytree(ALLURE_HISTORY_PATH, history_dest)
        print("> Historial de trends copiado para Allure")
    else:
        print("> No se encontró historial previo (primera ejecución)")


class AllurePlugin:
    """Plugin de Allure: screenshots automáticos y metadata del reporte."""

    @PluginSpec.hookimpl
    def before_all(self):
        load_dotenv(dotenv_path='.env')
        os.makedirs(ALLURE_RESULTS_PATH, exist_ok=True)
        copy_history_for_trends()

    @PluginSpec.hookimpl
    def after_step(self, context):
        attachment_screenshot_step_in_allure(context)

    @PluginSpec.hookimpl
    def after_all(self, context):
        generate_environment_properties()
        generate_executor_json()
