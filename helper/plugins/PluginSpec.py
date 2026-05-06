"""
=============================================================================
Módulo: PluginSpec.py
Descripción: Define la especificación de hooks (ganchos) del framework.
             Utiliza la librería 'pluggy' para implementar un sistema de plugins
             que permite extender el comportamiento de Behave sin modificar
             el código base.

Concepto clave:
    - hookspec: Marca un método como "especificación" (contrato/interfaz).
                Define QUÉ hooks existen y qué parámetros reciben.
    - hookimpl: Marca un método como "implementación" de un hook.
                Define QUÉ HACE cada hook cuando se ejecuta.

    Esto sigue el patrón de diseño "Plugin Architecture":
    1. Se definen las especificaciones (este archivo)
    2. Se implementan en plugins concretos (SeleniumPlugin, AllurePlugin)
    3. Se registran en el PluginManager (environment.py)
=============================================================================
"""

import pluggy  # Librería para crear sistemas de plugins extensibles

# Decorador para marcar métodos como ESPECIFICACIONES de hooks
# "hooks" es el nombre del proyecto/namespace que agrupa todos los hooks
hookspec = pluggy.HookspecMarker("hooks")

# Decorador para marcar métodos como IMPLEMENTACIONES de hooks
# Debe usar el mismo namespace ("hooks") para que pluggy los conecte
hookimpl = pluggy.HookimplMarker("hooks")


class PluginSpec:
    """
    Clase que define la ESPECIFICACIÓN (contrato) de todos los hooks disponibles.

    Cada método decorado con @hookspec define un punto de extensión que los
    plugins pueden implementar. Es como una "interfaz" en Java o un "protocolo"
    en Swift.

    Los hooks siguen el ciclo de vida de Behave:
        before_all → before_feature → before_scenario → before_step
        [ejecución del step]
        after_step → after_scenario → after_feature → after_all

    Cualquier plugin que implemente estos métodos con @hookimpl será
    ejecutado automáticamente en el momento correspondiente.
    """

    @hookspec
    def before_all(self, context):
        """
        Se ejecuta UNA VEZ antes de todas las pruebas.
        Útil para: configuración global, conexiones a BD, carga de datos.

        Args:
            context: Objeto compartido de Behave que persiste durante toda la ejecución.
        """

    @hookspec
    def after_all(self, context):
        """
        Se ejecuta UNA VEZ después de todas las pruebas.
        Útil para: limpieza global, cierre de conexiones, generación de reportes.

        Args:
            context: Objeto compartido de Behave.
        """

    @hookspec
    def before_scenario(self, context, scenario):
        """
        Se ejecuta ANTES de cada escenario (Scenario/Scenario Outline).
        Útil para: inicializar el navegador, preparar datos de prueba.

        Args:
            context: Objeto compartido de Behave.
            scenario: Objeto con información del escenario actual (nombre, tags, etc.)
        """

    @hookspec
    def after_scenario(self, context, scenario):
        """
        Se ejecuta DESPUÉS de cada escenario.
        Útil para: cerrar el navegador, limpiar datos, registrar resultados.

        Args:
            context: Objeto compartido de Behave.
            scenario: Objeto con información del escenario (incluye status: passed/failed).
        """

    @hookspec
    def after_feature(self, context, feature):
        """
        Se ejecuta DESPUÉS de cada feature (archivo .feature completo).
        Útil para: limpieza a nivel de feature, reportes parciales.

        Args:
            context: Objeto compartido de Behave.
            feature: Objeto con información del feature (nombre, escenarios, tags).
        """

    @hookspec
    def before_feature(self, context, feature):
        """
        Se ejecuta ANTES de cada feature.
        Útil para: preparación de datos específicos del feature.

        Args:
            context: Objeto compartido de Behave.
            feature: Objeto con información del feature.
        """

    @hookspec
    def after_step(self, context, step):
        """
        Se ejecuta DESPUÉS de cada step (Given/When/Then).
        Útil para: capturas de pantalla, logging, evidencia.

        Args:
            context: Objeto compartido de Behave.
            step: Objeto con información del step (nombre, status, duración).
        """

    @hookspec
    def before_step(self, context, step):
        """
        Se ejecuta ANTES de cada step.
        Útil para: logging, preparación previa al step.

        Args:
            context: Objeto compartido de Behave.
            step: Objeto con información del step.
        """

    @hookspec
    def after_tag(self, context, tag):
        """
        Se ejecuta DESPUÉS de procesar un tag específico.
        Útil para: lógica condicional basada en tags (@smoke, @regresion).

        Args:
            context: Objeto compartido de Behave.
            tag: String con el nombre del tag (sin @).
        """

    @hookspec
    def before_tag(self, context, tag):
        """
        Se ejecuta ANTES de procesar un tag específico.
        Útil para: configuración condicional según tags.

        Args:
            context: Objeto compartido de Behave.
            tag: String con el nombre del tag (sin @).
        """
