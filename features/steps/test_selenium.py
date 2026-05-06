"""
Módulo: test_selenium.py
Descripción: Steps de Behave que conectan los escenarios Gherkin con Selenium.
"""

import os

from assertpy import soft_assertions
from behave import given, when, then

from helper.pages.page_hakatoolsl import PageModel


@given(u'ingreso a hakatools')
def ingreso_a_hakatools(context):
    context.browser.get(os.getenv("URL"))


@when(u'selecciono la lista "{nombre_card}"')
def seleccionar_lista(context, nombre_card):
    context.elements._implicity_wait(element_by=PageModel.card_element).click()


@when(u'ingreso nombre de usuario "{nombre}"')
def seleccionar_nombre(context, nombre):
    context.elements._implicity_wait(element_by=PageModel.txt_first_name).send_keys(nombre)


@when(u'ingreso correo "{correo}"')
def seleccionar_correo(context, correo):
    context.elements._implicity_wait(element_by=PageModel.txt_email).send_keys(correo)


@when(u'ingreso direccion "{direccion}"')
def seleccionar_direccion(context, direccion):
    context.elements._implicity_wait(element_by=PageModel.txt_direccion).send_keys(direccion)


@when(u'ingreso direccion permanente "{direccion_permanente}"')
def seleccionar_direccion_permanente(context, direccion_permanente):
    context.elements._implicity_wait(element_by=PageModel.txt_direccion_permanente).send_keys(direccion_permanente)


@when(u'selecciono opcion enviar')
def seleccionar_enviar(context):
    context.elements._implicity_wait(element_by=PageModel.btn_enviar).click()


@then(u'valido resultados de formulario "{nombre}""{correo}""{direccion}""{direccion_permanente}"')
def validar_formulario(context, nombre, correo, direccion, direccion_permanente):
    resultado = context.elements._implicity_wait(element_by=PageModel.txt_result_form).text

    with soft_assertions():
        assert nombre in resultado, "el campo nombre del formulario no coincide"
        assert correo in resultado, "el campo correo del formulario no coincide"
        assert direccion in resultado, "el campo direccion del formulario no coincide"
        assert direccion_permanente in resultado, "el campo direccion permanente del formulario no coincide"
