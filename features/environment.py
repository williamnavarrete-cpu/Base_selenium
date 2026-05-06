"""
Módulo: environment.py
Descripción: Hooks de Behave. Delega al sistema de plugins (pluggy).
"""

import pluggy

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
