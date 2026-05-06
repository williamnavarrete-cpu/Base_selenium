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

Ciclo de vida de Behave:
    before_all → before_feature → before_tag → before_scenario → before_step
    [ejecución del step]
    after_step → after_scenario → after_tag → after_feature → after_all
=============================================================================
"""

import pluggy
from dotenv import load_dotenv

from helper.plugins.AllurePlugin import AllurePlugin
from helper.plugins.PluginSpec import PluginSpec
from helper.plugins.SeleniumPlugin import SeleniumPlugin

pm = pluggy.PluginManager("hooks")
pm.add_hookspecs(PluginSpec)

pm.register(SeleniumPlugin())
pm.register(AllurePlugin())


def before_all(context):
    pm.hook.before_all(context=context)


def after_all(context):
    pm.hook.after_all(context=context)


def before_tag(context, tag):
    pm.hook.before_tag(context=context, tag=tag)


def after_tag(context, tag):
    pm.hook.after_tag(context=context, tag=tag)


def before_feature(context, feature):
    pm.hook.before_feature(context=context, feature=feature)


def after_feature(context, feature):
    pm.hook.after_feature(context=context, feature=feature)


def before_scenario(context, scenario):
    pm.hook.before_scenario(context=context, scenario=scenario)


def after_scenario(context, scenario):
    pm.hook.after_scenario(context=context, scenario=scenario)


def before_step(context, step):
    pm.hook.before_step(context=context, step=step)


def after_step(context, step):
    pm.hook.after_step(context=context, step=step)
