"""
Módulo: PluginSpec.py
Descripción: Especificación de hooks del framework usando pluggy.
             Define QUÉ hooks existen. Los plugins los implementan con @hookimpl.
"""

import pluggy

hookspec = pluggy.HookspecMarker("hooks")
hookimpl = pluggy.HookimplMarker("hooks")


class PluginSpec:
    """Contrato de hooks disponibles en el ciclo de vida de Behave."""

    @hookspec
    def before_all(self, context):
        """Se ejecuta UNA VEZ antes de todas las pruebas."""

    @hookspec
    def after_all(self, context):
        """Se ejecuta UNA VEZ después de todas las pruebas."""

    @hookspec
    def before_scenario(self, context, scenario):
        """Se ejecuta ANTES de cada escenario."""

    @hookspec
    def after_scenario(self, context, scenario):
        """Se ejecuta DESPUÉS de cada escenario."""

    @hookspec
    def after_feature(self, context, feature):
        """Se ejecuta DESPUÉS de cada feature."""

    @hookspec
    def before_feature(self, context, feature):
        """Se ejecuta ANTES de cada feature."""

    @hookspec
    def after_step(self, context, step):
        """Se ejecuta DESPUÉS de cada step (Given/When/Then)."""

    @hookspec
    def before_step(self, context, step):
        """Se ejecuta ANTES de cada step."""

    @hookspec
    def after_tag(self, context, tag):
        """Se ejecuta DESPUÉS de procesar un tag."""

    @hookspec
    def before_tag(self, context, tag):
        """Se ejecuta ANTES de procesar un tag."""
