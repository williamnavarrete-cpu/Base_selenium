"""
=============================================================================
Módulo: environment.py
Descripción: Archivo de configuración de hooks de Behave.
             Behave busca automáticamente este archivo en la carpeta features/
             y ejecuta las funciones definidas aquí en los momentos correspondientes
             del ciclo de vida de las pruebas.

Arquitectura de Plugins:
    Este archivo actúa como "puente" entre Behave y el sistema de plugins (pluggy).
    En lugar de escribir toda la lógica aquí, delega a plugins registrados:
    - SeleniumPlugin: gestiona el navegador
    - AllurePlugin: gestiona la reportería

    Esto permite agregar nuevos plugins sin modificar este archivo.
    Solo se necesita crear el plugin e importarlo/registrarlo aquí.

Ciclo de vida de Behave:
    before_all → before_feature → before_tag → before_scenario → before_step
    [ejecución del step]
    after_step → after_scenario → after_tag → after_feature → after_all
=============================================================================
"""

import pluggy  # Framework de plugins que conecta especificaciones con implementaciones
from dotenv import load_dotenv  # Carga variables de entorno desde .env

# Importación de los componentes del sistema de plugins
from helper.plugins.AllurePlugin import AllurePlugin      # Plugin de reportería
from helper.plugins.PluginSpec import PluginSpec          # Especificación (contrato) de hooks
from helper.plugins.SeleniumPlugin import SeleniumPlugin  # Plugin del navegador

# === CONFIGURACIÓN DEL PLUGIN MANAGER ===

# Crea el gestor de plugins con el namespace "hooks"
# Este namespace debe coincidir con el usado en HookspecMarker y HookimplMarker
pm = pluggy.PluginManager("hooks")

# Registra la ESPECIFICACIÓN: le dice a pluggy qué hooks existen
pm.add_hookspecs(PluginSpec)

# Registra las IMPLEMENTACIONES: plugins concretos que ejecutan lógica
# El orden de registro determina el orden de ejecución
pm.register(SeleniumPlugin())  # Primero: inicializa/cierra el navegador
pm.register(AllurePlugin())    # Segundo: captura evidencia y genera reportes


# === FUNCIONES HOOK DE BEHAVE ===
# Behave llama automáticamente a estas funciones en los momentos correspondientes.
# Cada función delega al PluginManager, que ejecuta todos los plugins registrados.


def before_all(context):
    """
    Se ejecuta UNA VEZ antes de iniciar cualquier prueba.
    Delega a: AllurePlugin.before_all() → carga .env
    """
    pm.hook.before_all(context=context)


def after_all(context):
    """
    Se ejecuta UNA VEZ después de finalizar todas las pruebas.
    Delega a: AllurePlugin.after_all() → genera environment.properties
    """
    pm.hook.after_all(context=context)


def before_tag(context, tag):
    """
    Se ejecuta antes de procesar un tag (@smoke, @regresion, etc.)
    Permite ejecutar lógica condicional según los tags del escenario.

    Args:
        tag (str): Nombre del tag sin el símbolo @ (ej: "Regresion")
    """
    pm.hook.before_tag(context=context, tag=tag)


def after_tag(context, tag):
    """
    Se ejecuta después de procesar un tag.

    Args:
        tag (str): Nombre del tag procesado.
    """
    pm.hook.after_tag(context=context, tag=tag)


def before_feature(context, feature):
    """
    Se ejecuta antes de cada archivo .feature.

    Args:
        feature: Objeto Feature con nombre, descripción y escenarios.
    """
    pm.hook.before_feature(context=context, feature=feature)


def after_feature(context, feature):
    """
    Se ejecuta después de cada archivo .feature.

    Args:
        feature: Objeto Feature con resultados de todos sus escenarios.
    """
    pm.hook.after_feature(context=context, feature=feature)


def before_scenario(context, scenario):
    """
    Se ejecuta antes de cada escenario.
    Delega a: SeleniumPlugin.before_scenario() → carga .env e inicializa navegador.

    Args:
        scenario: Objeto Scenario con nombre, tags y steps.
    """
    pm.hook.before_scenario(context=context, scenario=scenario)


def after_scenario(context, scenario):
    """
    Se ejecuta después de cada escenario.
    Delega a: SeleniumPlugin.after_scenario() → cierra el navegador.

    Args:
        scenario: Objeto Scenario con status final (passed/failed/skipped).
    """
    pm.hook.after_scenario(context=context, scenario=scenario)


def before_step(context, step):
    """
    Se ejecuta antes de cada step (Given/When/Then/And).

    Args:
        step: Objeto Step con keyword, nombre y tabla de datos.
    """
    pm.hook.before_step(context=context, step=step)


def after_step(context, step):
    """
    Se ejecuta después de cada step.
    Delega a: AllurePlugin.after_step() → captura screenshot.

    Args:
        step: Objeto Step con status y duración de ejecución.
    """
    pm.hook.after_step(context=context, step=step)
