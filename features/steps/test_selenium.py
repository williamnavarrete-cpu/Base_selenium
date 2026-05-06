"""
=============================================================================
Módulo: test_selenium.py
Descripción: Definición de steps (pasos) para los escenarios de prueba.
             Cada función mapea un paso del archivo .feature (Gherkin) a
             código Python que interactúa con la aplicación.

Metodología BDD (Behavior-Driven Development):
    1. Se escribe el comportamiento esperado en lenguaje natural (.feature)
    2. Se implementan los steps que ejecutan las acciones
    3. Se ejecuta Behave que conecta el .feature con los steps

Decoradores de Behave:
    @given → Precondiciones (estado inicial del sistema)
    @when  → Acciones del usuario
    @then  → Verificaciones/aserciones (resultado esperado)

Parámetros entre comillas:
    En Gherkin: When ingreso nombre de usuario "Hakito"
    En Python:  @when(u'ingreso nombre de usuario "{nombre}"')
    Behave extrae "Hakito" y lo pasa como argumento 'nombre' a la función.
=============================================================================
"""

import os    # Acceso a variables de entorno (URL de la aplicación)
import time  # Utilidades de tiempo (pausas, si se necesitan)

from assertpy import soft_assertions  # Librería para aserciones suaves (múltiples validaciones)
from behave import given, when, then  # Decoradores que conectan Gherkin con Python

from helper.pages.page_hakatoolsl import PageModel  # Page Object con los localizadores


@given(u'ingreso a hakatools')
def ingreso_a_hakatools(context):
    """
    Step GIVEN: Navega a la URL de la aplicación HakaTools.

    Este es el paso de precondición que abre el navegador en la URL configurada.
    La URL se lee de la variable de entorno "URL" definida en el archivo .env

    Args:
        context: Objeto de Behave con context.browser (WebDriver) disponible.

    Ejemplo en .feature:
        Given ingreso a hakatools
    """
    # _go_to_url navega el browser a la URL especificada
    # os.getenv("URL") lee la URL desde las variables de entorno (.env)
    context.browser.get(os.getenv("URL"))


@when(u'selecciono la lista "{nombre_card}"')
def seleccionar_lista(context, nombre_card):
    """
    Step WHEN: Hace click en la tarjeta/card especificada.

    Busca el elemento card_element definido en PageModel y hace click.
    El parámetro nombre_card viene del .feature pero en este caso se usa
    un localizador fijo (PageModel.card_element).

    Args:
        context: Objeto de Behave con context.elements (clase Elements).
        nombre_card (str): Nombre de la card extraído del .feature (ej: "Formularios").

    Ejemplo en .feature:
        When selecciono la lista "Formularios"
    """
    # _implicity_wait busca el elemento con espera explícita y retorna el WebElement
    # .click() ejecuta un click sobre el elemento encontrado
    context.elements._implicity_wait(element_by=PageModel.card_element).click()


@when(u'ingreso nombre de usuario "{nombre}"')
def seleccionar_nombre(context, nombre):
    """
    Step WHEN: Escribe el nombre de usuario en el campo correspondiente.

    Args:
        context: Objeto de Behave con context.elements.
        nombre (str): Texto a escribir en el campo (ej: "Hakito").

    Ejemplo en .feature:
        And ingreso nombre de usuario "Hakito"
    """
    # send_keys() simula la escritura de texto en un campo input
    context.elements._implicity_wait(element_by=PageModel.txt_first_name).send_keys(nombre)


@when(u'ingreso correo "{correo}"')
def seleccionar_correo(context, correo):
    """
    Step WHEN: Escribe el correo electrónico en el campo email.

    Args:
        context: Objeto de Behave con context.elements.
        correo (str): Email a ingresar (ej: "hakito@hakalab.com").

    Ejemplo en .feature:
        And ingreso correo "hakito@hakalab.com"
    """
    context.elements._implicity_wait(element_by=PageModel.txt_email).send_keys(correo)


@when(u'ingreso direccion "{direccion}"')
def seleccionar_direccion(context, direccion):
    """
    Step WHEN: Escribe la dirección actual en el campo correspondiente.

    Args:
        context: Objeto de Behave con context.elements.
        direccion (str): Dirección a ingresar (ej: "calle prueba 123").

    Ejemplo en .feature:
        And ingreso direccion "calle prueba 123"
    """
    context.elements._implicity_wait(element_by=PageModel.txt_direccion).send_keys(direccion)


@when(u'ingreso direccion permanente "{direccion_permanente}"')
def seleccionar_direccion_permanente(context, direccion_permanente):
    """
    Step WHEN: Escribe la dirección permanente en el campo correspondiente.

    Args:
        context: Objeto de Behave con context.elements.
        direccion_permanente (str): Dirección permanente a ingresar.

    Ejemplo en .feature:
        And ingreso direccion permanente "calle permanente prueba 123"
    """
    context.elements._implicity_wait(element_by=PageModel.txt_direccion_permanente).send_keys(direccion_permanente)


@when(u'selecciono opcion enviar')
def seleccionar_enviar(context):
    """
    Step WHEN: Hace click en el botón de enviar formulario.

    Args:
        context: Objeto de Behave con context.elements.

    Ejemplo en .feature:
        And selecciono opcion enviar
    """
    context.elements._implicity_wait(element_by=PageModel.btn_enviar).click()


@then(u'valido resultados de formulario "{nombre}""{correo}""{direccion}""{direccion_permanente}"')
def validar_formulario(context, nombre, correo, direccion, direccion_permanente):
    """
    Step THEN: Valida que los datos ingresados aparezcan en el resultado del formulario.

    Utiliza "soft assertions" de la librería assertpy. A diferencia de un assert
    normal que detiene la ejecución en el primer fallo, soft_assertions ejecuta
    TODAS las validaciones y reporta TODOS los fallos al final.

    Esto es útil para validar múltiples campos de un formulario de una sola vez.

    Args:
        context: Objeto de Behave con context.elements.
        nombre (str): Nombre esperado en el resultado.
        correo (str): Correo esperado en el resultado.
        direccion (str): Dirección esperada en el resultado.
        direccion_permanente (str): Dirección permanente esperada.

    Ejemplo en .feature:
        Then valido resultados de formulario "Hakito""hakito@hakalab.com""calle prueba 123""calle permanente prueba 123"

    Lógica:
        1. Obtiene el texto del contenedor de resultados
        2. Verifica que cada dato ingresado esté presente en el texto
        3. Si alguno falla, el mensaje indica qué campo no coincide
    """
    # Obtiene el texto completo del div de resultados
    resultado = context.elements._implicity_wait(element_by=PageModel.txt_result_form).text

    # soft_assertions() permite ejecutar múltiples asserts sin detenerse en el primero que falle
    # Al salir del bloque with, reporta TODOS los fallos encontrados
    with soft_assertions():
        assert nombre in resultado, "el campo nombre del formulario no coincide"
        assert correo in resultado, "el campo correo del formulario no coincide"
        assert direccion in resultado, "el campo direccion del formulario no coincide"
        assert direccion_permanente in resultado, "el campo direccion permanente del formulario no coincide"
